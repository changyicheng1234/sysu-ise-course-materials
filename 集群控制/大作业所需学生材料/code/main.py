import json
import math
import time
from my_udp import UDPClient


class Control:
    def __init__(self):
        # 配置网络参数，格式: "<vehicle_name>,<server_ip>,<udp_port>,<udp_send_port>"
        net = "8T2wNKVWmryQVoC4Pcy3wKwKFCEt,192.168.206.1,3908,3909"  # 请替换为实际的网络配置

        # 解析net字符串
        params = net.split(',')
        if len(params) != 4:
            raise ValueError("Invalid net format. Expected: '<vehicle_name>,<server_ip>,<udp_port>,<udp_send_port>'")

        vehicle_name, server_ip, udp_port, udp_send_port = params
        udp_port = int(udp_port)
        udp_send_port = int(udp_send_port)

        # 初始化UDP客户端
        self.udp_client = UDPClient(server_ip, udp_port, udp_send_port, vehicle_name)

        self.m_v = 0
        self.m_x = 0
        self.m_y = 0
        self.m_yaw = 0

        self.control_rate = 10  # hz

    def control_node(self):
        start_time = time.time()
        while True:
            vehicle_data = self.udp_client.get_vehicle_state()
            self.m_x = vehicle_data.x
            self.m_y = vehicle_data.y
            self.m_yaw = vehicle_data.yaw / 180 * math.pi

            v, w = 10, 0  # 这里可以替换为你的控制算法
            self.udp_client.send_control_command(v, w)

            elapsed_time = time.time() - start_time
            sleep_time = max((1.0 / self.control_rate) - elapsed_time, 0.0)
            time.sleep(sleep_time)
            start_time = time.time()


if __name__ == '__main__':
    control = Control()
    control.udp_client.start()
    control.control_node()