import json
import math
import time
from my_udp import UDPClient
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import signal
import sys
import keyboard

class Control:
    def __init__(self):
        net = "8T2wNKVWmryQVoC4Pcy3wKwKFCEt,192.168.206.1,7348,7349"
        self.udp_client = UDPClient("192.168.206.1",7348,7349, "8T2wNKVWmryQVoC4Pcy3wKwKFCEt")

        self.m_v = 0
        self.m_x = 0
        self.m_y = 0
        self.m_yaw = 0

        self.control_rate = 10  # Hz

        # 轨迹数据存储
        self.trajectory_x = []
        self.trajectory_y = []
        
        # 轨迹绘图初始化（在主线程中创建）
        self.fig, self.ax = plt.subplots()
        self.x_data, self.y_data = [], []
        self.line, = self.ax.plot([], [], 'b-', lw=2)
        self.point, = self.ax.plot([], [], 'ro', markersize=8)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_title('Vehicle Trajectory')
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')

        # 控制参数
        self.current_speed = 0.0
        self.steering = 0.0
        self.acceleration = 3.0
        self.brake_deceleration = 3.0
        self.max_speed = 20.0
        self.min_speed = -10.0
        self.steering_speed = 0.55

        # 注册信号处理
        signal.signal(signal.SIGINT, self.save_and_exit)
        signal.signal(signal.SIGTERM, self.save_and_exit)
        
        # 注册保存快捷键
        keyboard.add_hotkey('ctrl+s', self.save_trajectory)

    def init_plot(self):
        self.line.set_data([], [])
        self.point.set_data([], [])
        return self.line, self.point

    def update_plot(self, frame):
        self.line.set_data(self.x_data, self.y_data)
        self.point.set_data(self.m_x, self.m_y)
        if self.x_data:
            x_min, x_max = min(self.x_data), max(self.x_data)
            y_min, y_max = min(self.y_data), max(self.y_data)
            margin = 2.0
            self.ax.set_xlim(x_min - margin, x_max + margin)
            self.ax.set_ylim(y_min - margin, y_max + margin)
        return self.line, self.point

    def save_trajectory(self):
        """保存轨迹到JSON文件"""
        if not self.trajectory_x:
            print("没有轨迹数据可保存")
            return
            
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"trajectory_{timestamp}.json"
        
        trajectory_data = {
            "X": self.trajectory_x,
            "Y": self.trajectory_y
        }
        
        with open(filename, 'w') as f:
            json.dump(trajectory_data, f, indent=2)
            
        print(f"轨迹已保存至 {filename}")
        
        # 同时保存图片
        img_filename = f"trajectory_{timestamp}.png"
        self.fig.savefig(img_filename, dpi=300)
        print(f"轨迹图片已保存至 {img_filename}")

    def save_and_exit(self, signum, frame):
        """保存轨迹并退出程序"""
        print("\n保存轨迹并退出...")
        if self.trajectory_x:
            self.save_trajectory()
        sys.exit(0)

    def control_node(self):
        # 在主线程中启动动画
        self.ani = FuncAnimation(
            self.fig, self.update_plot, init_func=self.init_plot,
            interval=100, blit=True, cache_frame_data=False
        )
        start_time = time.time()
        try:
            while True:
                # 获取车辆状态
                vehicle_data = self.udp_client.get_vehicle_state()
                self.m_x = vehicle_data.x
                self.m_y = vehicle_data.y
                self.m_yaw = vehicle_data.yaw / 180 * math.pi

                # 记录轨迹
                self.x_data.append(self.m_x)
                self.y_data.append(self.m_y)
                self.trajectory_x.append(self.m_x)
                self.trajectory_y.append(self.m_y)

                # 处理键盘输入
                dt = 1.0 / self.control_rate
                if keyboard.is_pressed('w'):
                    self.current_speed += self.acceleration * dt
                elif keyboard.is_pressed('s'):
                    self.current_speed -= self.brake_deceleration * dt
                self.current_speed = max(min(self.current_speed, self.max_speed), self.min_speed)

                # 转向控制
                if keyboard.is_pressed('a'):
                    self.steering = self.steering_speed
                elif keyboard.is_pressed('d'):
                    self.steering = -self.steering_speed
                else:
                    self.steering = 0.0

                # 发送控制指令
                self.udp_client.send_control_command(self.current_speed, self.steering)

                # 更新绘图事件（通过 Matplotlib 内部机制处理）
                plt.pause(0.001)  # 允许图形界面处理事件

                # 控制频率
                elapsed_time = time.time() - start_time
                sleep_time = max((1.0 / self.control_rate) - elapsed_time, 0.0)
                time.sleep(sleep_time)
                start_time = time.time()

        except Exception as e:
            print(f"错误发生: {e}")
            self.save_and_exit(None, None)

if __name__ == '__main__':
    control = Control()
    control.udp_client.start()
    control.control_node()  # 直接在主线程中运行控制节点
    plt.show()  # 主线程中启动图形界面