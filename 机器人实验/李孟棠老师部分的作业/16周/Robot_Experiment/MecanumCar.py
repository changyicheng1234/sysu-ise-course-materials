import sys
sys.path.append('/home/pi/Desktop/Robot_Experiment/Lib/')
import time
import UartServer

'''
通过串口发送指令控制电机的转速,时间
参数：
speed_l1---左前轮
speed_r1---右前轮
speed_l2---左后轮
speed_r2---右后轮
(-1000~1000)负值后退，正值前进，绝对值越大转速越高。
time 代表车轮转动时间，0代表一直转动，1000代表转动1秒，以此类推。
'''
#小车运行
def run(speed_l1,speed_r1,speed_l2,speed_r2,time):
    Car_Control_Cmd = '#006P{0:0>4d}T{4:0>4d}!#007P{1:0>4d}T{4:0>4d}!#008P{2:0>4d}T{4:0>4d}!#009P{3:0>4d}T{4:0>4d}!'.format(1500+speed_l1,1500-speed_r1,1500+speed_l2,1500-speed_r2,time)
    print(Car_Control_Cmd)
    UartServer.uart_send_str(Car_Control_Cmd)

#小车停止
def stop():
    run(0,0,0,0,1000) #

#小车前进
def forward(velocity,time):
    run(velocity,velocity,velocity,velocity,time) #

#小车后退
def backward(velocity,time):
    run(-velocity,-velocity,-velocity,-velocity,time) #

#小车左平移
def move_left(velocity,time):
    run(-velocity,velocity,velocity,-velocity,time) #

#小车右平移 
def move_right(velocity,time):
    run(velocity,-velocity,-velocity,velocity,time) #

#小车左旋转 
def turn_left(velocity,time):
    run(-velocity,velocity,-velocity,velocity,time) #

#小车右旋转
def turn_right(velocity,time):
    run(velocity,-velocity,velocity,-velocity,time) #

#测试函数
def test():
    forward(700,1000) #前进
    time.sleep(2)
    backward(700,1000) #后退
    time.sleep(2)
    move_left(700,1000)
    time.sleep(2)
    move_right(700,1000)
    time.sleep(2)
    turn_left(700,1000)
    time.sleep(2)
    turn_right(700,1000)
    time.sleep(2)
    stop()
    
if __name__ == '__main__':
    UartServer.setup_uart(115200) #设置串口
    test()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        destory() 
    
    
    
    