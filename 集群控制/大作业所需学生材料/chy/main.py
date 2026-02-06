import json
import math
import time
import logging
import os
import numpy as np # 新增：用于LQR避障相关的数值计算

# 从 my_udp.py 导入 VehicleData 和 UDPClient
from my_udp import VehicleData, UDPClient

# 为 main 模块设置一个独立的 logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main_control')
# logger.setLevel(logging.DEBUG) # 如果想看所有调试信息，可以设置为 DEBUG

class PIDController:
    """
    一个简单的PID控制器实现。
    """
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.prev_error = 0
        self.last_time = time.time()
        self.max_integral = 10.0  # 积分饱和上限
        self.min_integral = -10.0 # 积分饱和下限

        logger.info(f"PIDController initialized with Kp={self.kp}, Ki={self.ki}, Kd={self.kd}, Setpoint={self.setpoint}")

    def compute(self, current_value):
        """
        计算PID控制器的输出。
        Args:
            current_value (float): 当前的测量值。
        Returns:
            float: PID控制器的输出。
        """
        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0:
            dt = 1e-6  # 防止除零或时间倒流

        error = self.setpoint - current_value
        self.integral += error * dt

        # 积分防饱和（Integral wind-up prevention）
        self.integral = max(self.min_integral, min(self.max_integral, self.integral))

        # 微分项计算，防止在第一次计算时 prev_error 为 None
        derivative = (error - self.prev_error) / dt if self.prev_error is not None else 0

        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        self.prev_error = error
        self.last_time = current_time

        logger.debug(f"PID Compute: Current Value={current_value:.2f}, Error={error:.2f}, PID Output={output:.2f}")
        return output

    def set_setpoint(self, new_setpoint):
        """
        设置新的目标值。
        """
        self.setpoint = new_setpoint
        logger.info(f"PIDController setpoint updated to: {new_setpoint}")

    def reset(self):
        """
        重置PID控制器的内部状态。
        """
        self.integral = 0
        self.prev_error = 0
        self.last_time = time.time()
        logger.info("PIDController state reset.")


class Control:
    """
    智能车路径追踪控制类。
    """
    def __init__(self):
        self.logger = logging.getLogger("Control")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        self.logger.propagate = False

        # 网络配置
        # 这里使用LQR代码中提供的网络配置，因为它包含了name
        net = "8T2wNKVWmryQVoC4Pcy3wKwKFCEt,192.168.206.1,1254,1255"
        params = net.split(',')
        if len(params) != 4:
            raise ValueError("无效的网络格式，应为：<vehicle_name>,<server_ip>,<udp_port>,<udp_send_port>")
        vehicle_name, server_ip, udp_port, udp_send_port = params
        udp_port = int(udp_port)
        udp_send_port = int(udp_send_port)

        # 初始化 UDP 客户端 (从 my_udp.py 导入)
        self.udp_client = UDPClient(server_ip, udp_port, udp_send_port, vehicle_name)
        self.logger.info(f"Initialized UDP Client for vehicle: {vehicle_name} at {server_ip}:{udp_port}/{udp_send_port}")

        # 车辆状态（从 UDP 客户端获取）
        self.m_v = 0.0
        self.m_x = 0.0
        self.m_y = 0.0
        self.m_yaw = 0.0 # 弧度
        self.current_path_idx = 0 # 追踪路径时的当前索引

        # 车辆物理参数
        self.wheelbase = 2.86 # 轴距 L（米）

        # 控制参数
        self.control_rate = 50  # Hz
        self.max_speed_limit = 25.0 # 规定限速 25 m/s

        # Pure Pursuit 算法参数
        self.min_lookahead = 3.0
        self.max_lookahead = 20.0
        self.lookahead_gain = 1.0

        self.max_steering = math.radians(60) # 最大转向角（弧度）

        # PID 速度控制器
        self.speed_pid = PIDController(kp=1.0, ki=0.1, kd=0.05, setpoint=self.max_speed_limit)
        self.logger.info(f"Speed PID initialized with setpoint={self.speed_pid.setpoint} m/s")

        # 弯道速度调整参数
        self.min_turn_speed = 6.0 # 弯道最低允许速度 (m/s)
        self.curvature_speed_factor = 0.5 # 0到1之间，越大弯道减速越激进

        # === 避障相关参数（从新代码中提取）===
        self.obstacle_detection_range = 20.0 # 检测前方障碍物的距离阈值 (米)
        self.obstacle_stop_angle_threshold = math.radians(10) # 障碍物在前方角度阈值 (弧度)

        # 加载参考路径
        self.path = self.load_path_from_json("D:\\学习\\大三下\\集群控制\\学生材料\\chy\\ref_route.json")

        # 新增：目标点和标志位
        self.target_point = (22.02911949157715, 144.0296630859375)
        self.target_point_reached = False
        self.target_point_threshold = 5.0 # 达到目标点的距离阈值（米）


    def load_path_from_json(self, file_path):
        """
        从 JSON 文件加载路径数据，支持 { "X": [...], "Y": [...] } 格式。
        如果加载失败，将抛出异常。
        """
        current_working_directory = os.getcwd()
        self.logger.info(f"当前工作目录: {current_working_directory}")
        self.logger.info(f"尝试加载的路径文件: {os.path.join(current_working_directory, file_path)}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                path_data_raw = json.load(f)

            if isinstance(path_data_raw, dict) and "X" in path_data_raw and "Y" in path_data_raw:
                xs = path_data_raw["X"]
                ys = path_data_raw["Y"]
                if len(xs) != len(ys):
                    raise ValueError("JSON 文件中 'X' 和 'Y' 数组长度不匹配。")

                path_data = [[x, y] for x, y in zip(xs, ys)]
                self.logger.info("成功解析 { 'X': [...], 'Y': [...] } 格式的路径文件。")
            elif isinstance(path_data_raw, list) and all(isinstance(p, list) and len(p) == 2 for p in path_data_raw):
                path_data = path_data_raw
                self.logger.info("成功解析 [[x, y], ...] 格式的路径文件。")
            else:
                raise ValueError("ref_route.json 格式错误，既不是 { 'X': [...], 'Y': [...] } 也不是 [[x, y], ...]。")

            if not path_data:
                raise ValueError("加载的路径为空。")

            self.logger.info(f"成功从 {file_path} 加载路径，共 {len(path_data)} 个点。")
            return path_data
        except FileNotFoundError:
            self.logger.critical(f"错误：路径文件 '{file_path}' 未找到。请确保文件存在于正确的位置。")
            raise # 重新抛出异常，阻止程序继续执行
        except json.JSONDecodeError as e:
            self.logger.critical(f"错误：'{file_path}' 中的 JSON 格式无效: {e}。请检查 JSON 文件的语法。")
            raise # 重新抛出异常
        except Exception as e:
            self.logger.critical(f"加载路径失败: {e}。")
            raise # 重新抛出异常


    def find_closest_point(self, x, y):
        """
        寻找路径中距离当前车辆位置最近的路点。
        """
        min_dist = float('inf')
        closest_idx = 0
        # 优化：只在当前路径索引附近搜索，提高效率
        search_range_start = max(0, self.current_path_idx - 50)
        search_range_end = min(len(self.path), self.current_path_idx + 200) # 适当增加前向搜索范围

        for i in range(search_range_start, search_range_end):
            point = self.path[i]
            dist = math.sqrt((x - point[0])**2 + (y - point[1])**2)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        return closest_idx, min_dist

    def find_lookahead_point(self, x, y, yaw, lookahead_dist):
        """
        寻找前视点，从当前最近点向前搜索。
        Args:
            x (float): 车辆当前 x 坐标。
            y (float): 车辆当前 y 坐标。
            yaw (float): 车辆当前航向角（弧度）。
            lookahead_dist (float): 目标前视距离。
        Returns:
            tuple: (lx, ly, lookahead_idx) 前视点的坐标和在路径中的索引。
        """
        num_path_points = len(self.path)
        # 从当前追踪索引开始向前搜索
        search_start_idx = self.current_path_idx
        
        # 遍历从当前索引开始的路径点，直到找到前视点或者遍历完所有点
        for i in range(search_start_idx, num_path_points):
            px, py = self.path[i]
            dist = math.sqrt((x - px)**2 + (y - py)**2)

            # 检查点是否在车辆前方（角度限制）
            angle_to_point = math.atan2(py - y, px - x)
            angle_diff = math.atan2(math.sin(angle_to_point - yaw), math.cos(angle_to_point - yaw))

            # 当距离大于等于前视距离且点大致在车辆前方时，即找到前视点
            if dist >= lookahead_dist and abs(angle_diff) < math.pi / 2:
                return px, py, i
        
        # 如果循环结束仍未找到，通常意味着已经接近路径末尾或偏离路径
        # 在非闭合路径的情况下，使用路径的最后一个点作为前视点是合理的选择
        self.logger.warning("未能在车辆前方找到前视点。使用路径的最后一个点作为替代。")
        return self.path[-1][0], self.path[-1][1], len(self.path) - 1


    def pure_pursuit_control(self, x, y, yaw, speed):
        """
        使用 Pure Pursuit 算法计算控制指令（线速度和转向角）。
        Args:
            x (float): 车辆当前 x 坐标。
            y (float): 车辆当前 y 坐标。
            yaw (float): 车辆当前航向角（弧度）。
            speed (float): 车辆当前线速度。
        Returns:
            tuple: (speed_command, steering_angle) 计算出的线速度和转向角（弧度）。
        """
        # 自适应前视距离：随速度变化
        lookahead_dist = max(self.min_lookahead, min(self.max_lookahead, self.lookahead_gain * speed))
        self.logger.debug(f"当前速度: {speed:.2f} m/s, 计算前视距离: {lookahead_dist:.2f} m")

        # 寻找前视点
        lx, ly, lookahead_idx = self.find_lookahead_point(x, y, yaw, lookahead_dist)
        self.current_path_idx = lookahead_idx
        self.logger.debug(f"前视点: ({lx:.2f}, {ly:.2f})，索引: {lookahead_idx}")

        # 将前视点转换到车辆自身坐标系
        dx = lx - x
        dy = ly - y

        rotated_dx = dx * math.cos(-yaw) - dy * math.sin(-yaw)
        rotated_dy = dx * math.sin(-yaw) + dy * math.cos(-yaw)

        # 计算 alpha 角（车辆航向与前视点方向之间的夹角）
        alpha = math.atan2(rotated_dy, rotated_dx)
        self.logger.debug(f"Alpha 角: {math.degrees(alpha):.2f} 度")

        # 计算转向角 delta
        delta = math.atan2(2 * self.wheelbase * math.sin(alpha), lookahead_dist)
        delta = max(-self.max_steering, min(self.max_steering, delta)) # 限制转向角
        self.logger.debug(f"计算转向角 (delta): {math.degrees(delta):.2f} 度")

        # ====================================================================
        # 速度调整逻辑
        # ====================================================================
        current_target_speed = self.max_speed_limit # 默认目标速度为最大限制速度

        # 1. 弯道速度调整
        # 将 alpha 转换为一个介于 0 和 1 之间的因子，表示弯道的急迫程度
        turn_severity = abs(alpha) / self.max_steering # 0 到 1 之间，1 表示最急转弯
        # 使用一个函数来映射 turn_severity 到目标速度
        current_target_speed = self.min_turn_speed + (self.max_speed_limit - self.min_turn_speed) * (1 - turn_severity**self.curvature_speed_factor)
        # 确保速度在合法范围内
        current_target_speed = max(self.min_turn_speed, min(self.max_speed_limit, current_target_speed))
        self.logger.debug(f"Alpha={math.degrees(alpha):.2f}, Turn Severity={turn_severity:.2f}, 动态弯道目标速度: {current_target_speed:.2f} m/s")

        # 2. 障碍物避障/拥堵检测
        try:
            front_vehicle = self.udp_client.get_front_vehicle_state()
            # 注意：front_vehicle.x/y 是全局坐标，self.m_x/y 也是全局坐标
            dx_f = front_vehicle.x - x # 使用车辆当前X
            dy_f = front_vehicle.y - y # 使用车辆当前Y
            distance_to_front = math.hypot(dx_f, dy_f)

            # 计算障碍物在车辆前方 ±10度角内
            angle_to_obstacle = math.atan2(dy_f, dx_f)
            # 计算车辆朝向与障碍物方向的夹角
            direction_diff = abs(math.atan2(math.sin(angle_to_obstacle - yaw), math.cos(angle_to_obstacle - yaw)))


            # 检查障碍物是否在前方指定距离和角度范围内
            if direction_diff < self.obstacle_stop_angle_threshold and distance_to_front < self.obstacle_detection_range:
                # 调整目标速度为0，实现停车避障
                current_target_speed = 0.0
                self.logger.warning(f"⚠️ 拥堵检测：前方车辆距离 {distance_to_front:.2f} m (角度 {math.degrees(direction_diff):.2f}°)，目标速度调整为 {current_target_speed:.2f} m/s")
        except Exception as e:
            # 如果没有检测到前车，或者有其他异常，则跳过避障逻辑
            self.logger.debug(f"未检测到正前方车辆进行避障：{e}")
            pass

        # 将最终确定的目标速度设置给 PID 控制器
        self.speed_pid.set_setpoint(current_target_speed)

        # 使用 PID 计算线速度指令
        speed_command = self.speed_pid.compute(speed)
        # 最终的速度指令也要受到总限速的约束
        speed_command = max(0.0, min(self.max_speed_limit, speed_command))
        self.logger.debug(f"PID计算出的线速度指令: {speed_command:.2f} m/s")

        return speed_command, delta

    def control_node(self):
        """
        主控制循环，周期性地获取车辆状态，计算控制指令并发送。
        """
        self.logger.info("等待初始车辆状态数据...")
        while True:
            initial_vehicle_data = self.udp_client.get_vehicle_state()
            if initial_vehicle_data.x != 0.0 or initial_vehicle_data.y != 0.0 or initial_vehicle_data.speed != 0.0:
                break
            time.sleep(0.1)

        self.current_path_idx, _ = self.find_closest_point(initial_vehicle_data.x, initial_vehicle_data.y)
        self.logger.info(f"车辆初始位置: ({initial_vehicle_data.x:.2f}, {initial_vehicle_data.y:.2f})。从路径索引: {self.current_path_idx} 开始追踪。")

        start_time = time.time()
        reach_flag = 1
        while True:
            try:
                # 获取车辆最新状态
                vehicle_data = self.udp_client.get_vehicle_state()
                self.m_x = vehicle_data.x
                self.m_y = vehicle_data.y
                self.m_yaw = vehicle_data.yaw / 180 * math.pi # 将度数转换为弧度
                self.m_v = vehicle_data.speed
                self.logger.debug(f"当前车辆状态: X={self.m_x:.2f}, Y={self.m_y:.2f}, Yaw={math.degrees(self.m_yaw):.2f} 度, Speed={self.m_v:.2f} m/s")

                # *** 新增的逻辑：检测是否到达指定点并修改路径 ***
                if not self.target_point_reached and reach_flag:
                    reach_flag = 0
                    target_x, target_y = self.target_point
                    dist_to_target = math.sqrt((self.m_x - target_x)**2 + (self.m_y - target_y)**2)
                    
                    if dist_to_target < self.target_point_threshold:
                        self.logger.info(f"✅ 检测到车辆已接近目标点 ({target_x:.2f}, {target_y:.2f})，距离 {dist_to_target:.2f} 米。")
                        
                        # 找到目标点在原始路径中的索引
                        target_point_idx = -1
                        for i, point in enumerate(self.path):
                            if abs(point[0] - target_x) < 0.001 and abs(point[1] - target_y) < 0.001: # 浮点数比较用小误差范围
                                target_point_idx = i
                                break
                        
                        if target_point_idx != -1:
                            # 保留目标点及之后的所有点
                            self.path = self.path[target_point_idx:]
                            self.current_path_idx = 0 # 重置当前路径索引为新路径的起点
                            self.target_point_reached = True
                            self.logger.info(f"路径已修改，从索引 {target_point_idx} 开始，剩余 {len(self.path)} 个点。")
                        else:
                            self.logger.warning(f"⚠️ 目标点 ({target_x}, {target_y}) 未在原始路径中找到，无法进行路径裁剪。")
                # *** 结束新增逻辑 ***

                # 计算控制指令（线速度 v, 角速度 w）
                # pure_pursuit_control 内部会根据弯道情况和避障逻辑动态调整目标速度
                v, w = self.pure_pursuit_control(self.m_x, self.m_y, self.m_yaw, self.m_v)

                # 发送控制指令
                self.udp_client.send_control_command(v, w)

                # 控制循环时间，确保以设定的频率运行
                elapsed_time = time.time() - start_time
                sleep_time = max((1.0 / self.control_rate) - elapsed_time, 0.0)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                start_time = time.time() # 为下一次循环重置时间
            except Exception as e:
                self.logger.critical(f"控制节点循环中发生错误: {e}")
                time.sleep(1.0 / self.control_rate) # 错误时也休眠，避免高 CPU 占用

if __name__ == '__main__':
    try:
        control = Control()
        control.udp_client.start() # 启动 UDP 接收线程
        control.control_node() # 启动主控制循环
    except Exception as e:
        logger.critical(f"程序启动失败或遇到致命错误: {e}")
        # 这里可以选择更优雅的退出方式，例如清理资源