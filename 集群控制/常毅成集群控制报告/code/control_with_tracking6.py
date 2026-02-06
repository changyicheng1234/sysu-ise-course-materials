import json
import math
import time
import numpy as np
from my_udp import UDPClient
import matplotlib.pyplot as plt
import threading
from numpy.linalg import inv

class Control:
    def __init__(self):
        net = {
            "ip": "192.168.206.1",
            "port": 7348,
            "send_port":7349,
            "vehicle_name": "8T2wNKVWmryQVoC4Pcy3wKwKFCEt"
        }
        self.udp_client = UDPClient(net["ip"], net["port"], net["send_port"], net["vehicle_name"])

        self.m_x = 0
        self.m_y = 0
        self.m_yaw = 0
        self.m_v = 0

        self.last_x = 0
        self.last_y = 0

        self.control_rate = 30  # Hz
        self.dt = 1.0 / self.control_rate
        
        # === 加载路径并稀疏化 ===
        with open("D:\\学习\\大三下\\集群控制\\学生材料\\学生材料\\ref_route.json", "r") as f:
            route = json.load(f)
            raw_x = route["X"]
            raw_y = route["Y"]
            self.path_x, self.path_y = self.sparsify_path(raw_x, raw_y, spacing=0.3)

        self.path_curvatures = self.compute_path_curvatures(self.path_x, self.path_y)

        self.wheel_base = 2.86
        self.target_velocity = 16

        self.trajectory_x = []
        self.trajectory_y = []
        self.running = True
        self.need_overtake = False
        self.in_overtake = False


    def sparsify_path(self, x, y, spacing=0.3):
        sparse_x, sparse_y = [x[0]], [y[0]]
        acc_dist = 0.0
        for i in range(1, len(x)):
            dx = x[i] - sparse_x[-1]
            dy = y[i] - sparse_y[-1]
            dist = math.hypot(dx, dy)
            if acc_dist + dist >= spacing:
                sparse_x.append(x[i])
                sparse_y.append(y[i])
                acc_dist = 0.0
            else:
                acc_dist += dist
        return sparse_x, sparse_y

    def compute_path_curvatures(self, x, y):
        curvatures = []
        for i in range(1, len(x) - 1):
            x1, y1 = x[i - 1], y[i - 1]
            x2, y2 = x[i], y[i]
            x3, y3 = x[i + 1], y[i + 1]

            a = math.hypot(x1 - x2, y1 - y2)
            b = math.hypot(x2 - x3, y2 - y3)
            c = math.hypot(x3 - x1, y3 - y1)

            if a * b * c == 0:
                curvatures.append(0.0)
            else:
                s = (a + b + c) / 2.0
                area = math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
                curvature = 4 * area / (a * b * c)
                curvatures.append(curvature)
        curvatures = [curvatures[0]] + curvatures + [curvatures[-1]]
        return curvatures

    def generate_overtake_path(self, start_index, offset=3.5, overtake_length=20.0):
        """
        从原路径中局部构造一段横向偏移轨迹（用于超车），并最终平滑回归原路径。
        - start_index: 当前起点索引
        - offset: 横向偏移量（米）
        - overtake_length: 超车段长度（米）
        """
        offset_x, offset_y = [], []
        merge_back_x, merge_back_y = [], []

        accumulated_dist = 0.0
        i = start_index
        while i < len(self.path_x) - 1 and accumulated_dist < overtake_length:
            # 局部路径方向
            dx = self.path_x[i + 1] - self.path_x[i]
            dy = self.path_y[i + 1] - self.path_y[i]
            yaw = math.atan2(dy, dx)

            # 添加偏移点
            ox = self.path_x[i] - offset * math.sin(yaw)
            oy = self.path_y[i] + offset * math.cos(yaw)
            offset_x.append(ox)
            offset_y.append(oy)

            accumulated_dist += math.hypot(dx, dy)
            i += 1

        # 插入一个“平滑回原始路径”的过渡段
        merge_steps = 20
        for j in range(merge_steps):
            alpha = j / (merge_steps - 1)
            blend_x = (1 - alpha) * offset_x[-1] + alpha * self.path_x[i]
            blend_y = (1 - alpha) * offset_y[-1] + alpha * self.path_y[i]
            merge_back_x.append(blend_x)
            merge_back_y.append(blend_y)

        # 拼接整个路径（前段 + 超车段 + 回归段 + 原路径剩余段）
        new_path_x = self.path_x[:start_index] + offset_x + merge_back_x + self.path_x[i+1:]
        new_path_y = self.path_y[:start_index] + offset_y + merge_back_y + self.path_y[i+1:]
        return new_path_x, new_path_y


    def control_node(self):
        start_time = time.time()
        while self.running:
            vehicle_data = self.udp_client.get_vehicle_state()
            self.m_x = vehicle_data.x
            self.m_y = vehicle_data.y
            self.m_yaw = vehicle_data.yaw / 180 * math.pi

            try:
                self.m_v = vehicle_data.speed
            except AttributeError:
                dx = self.m_x - self.last_x
                dy = self.m_y - self.last_y
                self.m_v = math.hypot(dx, dy) / self.dt

            self.last_x = self.m_x
            self.last_y = self.m_y

            self.trajectory_x.append(self.m_x)
            self.trajectory_y.append(self.m_y)

            print(f"位置: x={self.m_x:.2f}, y={self.m_y:.2f}, yaw={math.degrees(self.m_yaw):.2f}°, v={self.m_v:.2f} m/s")

            v, w = self.compute_control_command()
            self.udp_client.send_control_command(v, w)

            elapsed_time = time.time() - start_time
            time.sleep(max(self.dt - elapsed_time, 0.0))
            start_time = time.time()

        print("控制已结束，开始绘图...")
        self.plot_trajectory()

    def compute_control_command(self):

        # === 预估前方曲率，动态调整 lookahead 距离 ===
        est_index = self.find_target_index()
        curvature_ahead = self.path_curvatures[min(est_index, len(self.path_curvatures) - 1)]
        
        if curvature_ahead > 0.12:
            lookahead = 2.5
        elif curvature_ahead > 0.08:
            lookahead = 4.0
        elif curvature_ahead > 0.04:
            lookahead = 5.5
        else:
            lookahead = 6.0

        target_index = self.find_target_index(lookahead=lookahead)

        # === 减少多点平均导致的目标点前移 ===
        extend_count = 3
        acc_x, acc_y = 0.0, 0.0
        actual_count = 0
        for i in range(extend_count):
            idx = min(target_index + i, len(self.path_x) - 1)
            acc_x += self.path_x[idx]
            acc_y += self.path_y[idx]
            actual_count += 1
        tx = acc_x / actual_count
        ty = acc_y / actual_count

        # === 目标点后退偏移，防止进弯超前 & 出弯更靠前 ===
        target_yaw = math.atan2(ty - self.m_y, tx - self.m_x)
        backward_offset = 0.5
        if curvature_ahead < 0.05:
            backward_offset = 0.2  # 出弯或直线段，目标更贴近
        tx -= backward_offset * math.cos(target_yaw)
        ty -= backward_offset * math.sin(target_yaw)

        dx = tx - self.m_x
        dy = ty - self.m_y
        path_yaw = math.atan2(dy, dx)

        # === 横向误差计算 ===
        perp_vec = [-math.sin(path_yaw), math.cos(path_yaw)]
        e_y = dx * perp_vec[0] + dy * perp_vec[1]
        e_yaw = math.atan2(math.sin(path_yaw - self.m_yaw), math.cos(path_yaw - self.m_yaw))

        state = np.array([
            [e_y],
            [self.m_v * math.sin(e_yaw)],
            [e_yaw],
            [0.0]
        ])

        # === 动态限速：急弯降速，缓弯提速 ===
        if curvature_ahead > 0.12:
            desired_v = 8.0
        elif curvature_ahead > 0.08:
            desired_v = 9.0
        elif curvature_ahead > 0.04:
            desired_v = 10.0
        else:
            desired_v = 16

        alpha_v = 0.15
        self.target_velocity = (1 - alpha_v) * self.target_velocity + alpha_v * desired_v
        '''
        try:
            front_vehicle = self.udp_client.get_front_vehicle_state()
            dx_f = front_vehicle.x - self.m_x
            dy_f = front_vehicle.y - self.m_y
            distance_to_front = math.hypot(dx_f, dy_f)
            direction_diff = abs(math.atan2(dy_f, dx_f) - self.m_yaw)
            direction_diff = min(direction_diff, 2 * math.pi - direction_diff)

            slow_ahead = direction_diff < math.radians(15) and distance_to_front < 15 and front_vehicle.speed < 3.0

            safe_to_overtake = True
            oncoming_vehicles = self.udp_client.get_oncoming_vehicles()
            for veh in oncoming_vehicles:
                dx_o = veh.x - self.m_x
                dy_o = veh.y - self.m_y
                dist = math.hypot(dx_o, dy_o)
                yaw_to_o = math.atan2(dy_o, dx_o)
                rel_angle = abs(yaw_to_o - math.pi - self.m_yaw)
                rel_angle = min(rel_angle, 2 * math.pi - rel_angle)
                if dist < 25 and rel_angle < math.radians(25):
                    safe_to_overtake = False
                    break

            if slow_ahead and safe_to_overtake and not self.in_overtake:
                overtake_index = self.find_target_index(lookahead=5.0)
                self.path_x, self.path_y = self.generate_overtake_path(overtake_index)
                self.path_curvatures = self.compute_path_curvatures(self.path_x, self.path_y)
                self.in_overtake = True
                print("满足条件，开始超车")

        except Exception as e:
            print(f"超车判断失败：{e}")

        '''

        # === 拥堵检测：根据前车距离动态减速 ===
        try:
            front_vehicle = self.udp_client.get_front_vehicle_state()
            dx_f = front_vehicle.x - self.m_x
            dy_f = front_vehicle.y - self.m_y
            distance_to_front = math.hypot(dx_f, dy_f)

            direction_diff = abs(math.atan2(dy_f, dx_f) - self.m_yaw)
            direction_diff = min(direction_diff, 2 * math.pi - direction_diff)

            # 正前方 ±30°
            if direction_diff < math.radians(10) and distance_to_front < 20:
                self.target_velocity = 0#max(0.0, (distance_to_front - 4.0) * 0.5)
                print(f"⚠️ 拥堵检测：前方车辆距离 {distance_to_front:.2f} m，目标速度调整为 {self.target_velocity:.2f} m/s")
        except Exception as e:
            pass  # 没检测到前车则跳过

        v = max(self.m_v, 0)

        # === 线性系统建模（A, B） ===
        A = np.array([[0, 1, 0, 0],
                    [0, 0, v, 0],
                    [0, 0, 0, 1],
                    [0, 0, 0, 0]])
        B = np.array([[0],
                    [0],
                    [0],
                    [v / self.wheel_base]])

        # === LQR Q矩阵更新（强化横向误差） ===
        Q = np.diag([5.0, 0.0, 6.0, 0.0])
        R = np.array([[0.05]])

        K = self.solve_lqr(A, B, Q, R)
        u = -np.dot(K, state)
        w_lqr = float(u[0])

        # === 前馈角速度 ===
        alpha = math.atan2(dy, dx) - self.m_yaw
        alpha = math.atan2(math.sin(alpha), math.cos(alpha))
        curvature = 2 * math.sin(alpha) / max(math.hypot(dx, dy), 1e-3)
        w_ff = self.m_v * curvature

        gain = min(1.0, max(0.4, abs(curvature) * 1.0))
        w = w_lqr + gain * w_ff

        # === 放宽角速度限制（增强出弯恢复） ===
        w = max(min(w, 3.0), -3.0)

        return self.target_velocity, w




    def solve_lqr(self, A, B, Q, R):
        P = Q.copy()
        for _ in range(100):
            P_next = A.T @ P @ A - A.T @ P @ B @ inv(R + B.T @ P @ B) @ B.T @ P @ A + Q
            if np.allclose(P_next, P, atol=1e-3):
                break
            P = P_next
        K = inv(R + B.T @ P @ B) @ B.T @ P @ A
        return K

    def find_target_index(self, lookahead=6.0):
        min_dist = float("inf")
        nearest_index = 0
        for i in range(len(self.path_x)):
            dx = self.path_x[i] - self.m_x
            dy = self.path_y[i] - self.m_y
            dist = math.hypot(dx, dy)
            if dist < min_dist:
                min_dist = dist
                nearest_index = i

        total_dist = 0.0
        for i in range(nearest_index, len(self.path_x) - 1):
            dx = self.path_x[i + 1] - self.path_x[i]
            dy = self.path_y[i + 1] - self.path_y[i]
            total_dist += math.hypot(dx, dy)
            if total_dist >= lookahead:
                return i + 1
        return len(self.path_x) - 1

    def plot_trajectory(self):
        if self.trajectory_x and self.trajectory_y:
            if self.trajectory_x[0] == 0 and self.trajectory_y[0] == 0:
                self.trajectory_x.pop(0)
                self.trajectory_y.pop(0)

        plt.figure()
        plt.plot(self.path_x, self.path_y, '--', label='Target Path', color='gray')
        plt.plot(self.trajectory_x, self.trajectory_y, 'r-', label='Actual Trajectory')
        plt.title('LQR + Adaptive Feedforward Control + Dynamic Speed')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def listen_for_exit(self):
        input("▶ 按 Enter 键退出控制...\n")
        self.running = False

if __name__ == '__main__':
    control = Control()
    control.udp_client.start()
    threading.Thread(target=control.listen_for_exit, daemon=True).start()
    control.control_node()