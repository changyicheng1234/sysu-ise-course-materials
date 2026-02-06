import sys
sys.path.append('/home/pi/Desktop/Robot_Experiment/Lib/')
import time
import UartServer

'''
通过串口发送指令控制电机的转速,时间
参数：
speed:-1000~1000,负值后退，正值前进，绝对值越大转速越高。
time: 代表车轮转动时间，0代表一直转动，1000代表转动1秒，以此类推。
'''
#开始

#小车运行函数，请修改该函数使得该函数可以驱动四个电机旋转
def run(n,speed,_time):
    # n=[0,1,2,3,4,5,6] 分别代表停止、前进、后退、左移、右移、左旋转、右旋转七个基础功能
    if n == 1 or n == 0:
        Car_Control_Cmd = '#006P{0:0>4d}T{4:0>4d}!' \
                          '#007P{1:0>4d}T{4:0>4d}!' \
                          '#008P{2:0>4d}T{4:0>4d}!' \
                          '#009P{3:0>4d}T{4:0>4d}!' \
                          .format(1500+speed,1500-speed,1500+speed,1500-speed,_time)
        print("Forward")
        print(Car_Control_Cmd)
        UartServer.uart_send_str(Car_Control_Cmd)
    elif n == 2:
        Car_Control_Cmd = '#006P{0:0>4d}T{4:0>4d}!' \
                          '#007P{1:0>4d}T{4:0>4d}!' \
                          '#008P{2:0>4d}T{4:0>4d}!' \
                          '#009P{3:0>4d}T{4:0>4d}!' \
            .format(1500 - speed, 1500 + speed, 1500 - speed, 1500 + speed, _time)
        print("Backward")
        print(Car_Control_Cmd)
        UartServer.uart_send_str(Car_Control_Cmd)
    elif n== 3:
        Car_Control_Cmd = '#006P{0:0>4d}T{4:0>4d}!' \
                          '#007P{1:0>4d}T{4:0>4d}!' \
                          '#008P{2:0>4d}T{4:0>4d}!' \
                          '#009P{3:0>4d}T{4:0>4d}!' \
            .format(1500 - speed, 1500 - speed, 1500 + speed, 1500 + speed, _time)
        print("Shift Left")
        print(Car_Control_Cmd)
        UartServer.uart_send_str(Car_Control_Cmd)
    elif n == 4:
        Car_Control_Cmd = '#006P{0:0>4d}T{4:0>4d}!' \
                          '#007P{1:0>4d}T{4:0>4d}!' \
                          '#008P{2:0>4d}T{4:0>4d}!' \
                          '#009P{3:0>4d}T{4:0>4d}!' \
            .format(1500 + speed, 1500 + speed, 1500 - speed, 1500 - speed, _time)
        print("Shift Right")
        print(Car_Control_Cmd)
        UartServer.uart_send_str(Car_Control_Cmd)
    elif n == 5:
        Car_Control_Cmd = '#006P{0:0>4d}T{4:0>4d}!' \
                          '#007P{1:0>4d}T{4:0>4d}!' \
                          '#008P{2:0>4d}T{4:0>4d}!' \
                          '#009P{3:0>4d}T{4:0>4d}!' \
            .format(1500 - speed, 1500 - speed, 1500 - speed, 1500 - speed, _time)
        print("Turn Left")
        print(Car_Control_Cmd)
        UartServer.uart_send_str(Car_Control_Cmd)
    elif n == 6:
        Car_Control_Cmd = '#006P{0:0>4d}T{4:0>4d}!' \
                          '#007P{1:0>4d}T{4:0>4d}!' \
                          '#008P{2:0>4d}T{4:0>4d}!' \
                          '#009P{3:0>4d}T{4:0>4d}!' \
            .format(1500 + speed, 1500 + speed, 1500 + speed, 1500 + speed, _time)
        print("Turn Right")
        print(Car_Control_Cmd)
        UartServer.uart_send_str(Car_Control_Cmd)
    else:
        print("Wrong Input!")

#小车停止
def stop():
    run(0,0,1000)

#测试函数，请调用run函数来补充该函数，使得小车能够实现前进、后退、左平移、右平移、左旋转、右旋转
def test():
    run(1,500,1000)  # 前进
    time.sleep(2)
    run(2, 500, 1000)  # 后退
    time.sleep(2)
    run(3, 500, 1000)  # 左移
    time.sleep(2)
    run(4, 500, 1000)  # 右移
    time.sleep(2)
    run(5, 500, 1000)  # 左转
    time.sleep(2)
    run(6, 500, 1000)  # 右转
    time.sleep(2)
    stop()

#结束
    
if __name__ == '__main__':
    UartServer.setup_uart(115200) #设置串口
    test()
    try:
        while True:
            pass
    except KeyboardInterrupt:
       print("1")
    
    
    
    