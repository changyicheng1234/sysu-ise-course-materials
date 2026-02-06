#导入模块

import sys
sys.path.append('/home/pi/Desktop/Robot_Experiment/Lib/')
import time

import MecanumCar 
import Ultrasonic_sensor
import Beep 
import UartServer

systick_ms_bak = 0
during = 0.01
dis = 100

def setup_start():
    Beep.beep(3,0.1)

def obstacle_avoidance():
    global systick_ms_bak,during,dis
    #最少100ms执行一次
    if(int((time.time() * 1000))- systick_ms_bak > 100):
        systick_ms_bak = int((time.time() * 1000))
        #获取超声波传感器返回的高电平时间
        during = Ultrasonic_sensor.during_time()
        print(during)

        #开始
        #编写程序，使用超声波传感器的数据计算小车与障碍物的距离，然后根据距离大小执行相应的动作

        dist = during*340/2
        if dist >= 0.3:
            MecanumCar.run(1,500,1000)
        else:
            MecanumCar.run(5,500,1000)

        #结束

def obstacle_avoidance_new():
    global systick_ms_bak,during,dis
    #最少100ms执行一次
    if(int((time.time() * 1000))- systick_ms_bak > 100):
        systick_ms_bak = int((time.time() * 1000))
        #获取超声波传感器返回的高电平时间
        during = Ultrasonic_sensor.during_time()
        print(during)

        #开始
        #编写程序，使用超声波传感器的数据计算小车与障碍物的距离，然后根据距离大小执行相应的动作

        dist = during*340/2
        if dist <= 0.4:
            MecanumCar.run(0,0,1000)
        elif dist > 0.4 and dist < 0.6:
            MecanumCar.run(1,500,1000)
        else:
            MecanumCar.run(1,1000,1000)

        #结束

def destory():
    MecanumCar.stop()
    Beep.off()
    
if __name__ == '__main__':
     Beep.setup_beep()
     Ultrasonic_sensor.setup_sensor(23,22)   #初始化超声波
     UartServer.setup_uart(115200)           #设置串口
     setup_start()                           #初始化示意蜂鸣器滴滴滴三声
     try:
         while True:
             obstacle_avoidance()            #超声波避障
     except KeyboardInterrupt:
         print("1")
#       


# 
#      Beep.setup_beep()
#      Ultrasonic_sensor.setup_sensor(23, 22)  # 初始化超声波
#      UartServer.setup_uart(115200)  # 设置串口
#      setup_start()  # 初始化示意蜂鸣器滴滴滴三声
#      try:
#          while True:
#            obstacle_avoidance_new()  # 超声波直线跟随
#      except KeyboardInterrupt:
#           print("1")
#     #     destory()