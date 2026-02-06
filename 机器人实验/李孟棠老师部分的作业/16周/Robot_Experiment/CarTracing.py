#导入模块
import sys
sys.path.append('/home/pi/Desktop/Robot_Experiment/Lib/')
import cv2   #导入库
import Camera
import numpy as np
import time

import UartServer as myUart
import Beep as myBeep
import MecanumCar as myCar

color_dist = {
             'red':   {'Lower': np.array([0, 43, 35]), 'Upper': np.array([10, 255, 255])},
             'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
             'blue':  {'Lower': np.array([100, 43, 46]), 'Upper': np.array([124, 255, 255])},
             'white': {'Lower': np.array([0, 0, 180]), 'Upper': np.array([180, 30, 255])},
             'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 100])},
             'yellow':  {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
             }

cx = 0
cy = 0

#开始修改变量
cx_m = 0
cx_l = 0
cx_r = 0

area_L = 0
area_T = 0
#结束修改变量

#开始补充1
def Tracing(cx): 
    myCar.stop()  
#结束补充1
   
def car_tracking(frame,color):
    global cx,cy   
    #将图片缩放到 160*120
    frame = cv2.resize(frame,(160,120),interpolation = cv2.INTER_CUBIC)
    #高斯滤波
    frame = cv2.GaussianBlur(frame,(5,5),0) 
    #将图片的色域转换为HSV的样式 以便检测
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
    #设置阈值，去除背景 保留所设置的颜色
    mask = cv2.inRange(hsv, color_dist[color]['Lower'], color_dist[color]['Upper'])   
    #腐蚀
    mask = cv2.erode(mask,None,iterations=2) 
    #膨胀
    mask = cv2.dilate(mask, None, iterations=2)
    #高斯模糊
    mask = cv2.GaussianBlur(mask,(3,3),0) 
    #查找轮廓
    image,contours,hierarchy= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    #有检测到轮廓
    if len(contours) > 0:
        #取最大面积的轮廓
        c = max(contours,key=cv2.contourArea)
        #计算该轮廓图像的矩
        M = cv2.moments(c)
        #由矩计算面积和质心位置
        area = M['m00']
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(area, int(cx),int(cy))
        
        #开始补充2
        
        #结束补充2
            
    else:
        print("None line")
        pass
    return frame
 
if __name__ == '__main__':    
    myBeep.setup_beep()
    myUart.setup_uart(115200)
    
    #机械臂初始化
    myUart.uart_send_str('{#000P1500T1000!#001P1500T1000!#002P2200T1000!#003P0900T1000!#004P1500T1000!#005P1500T1000!}')
    
    cam = Camera.Camera()  #摄像头库实例化    
    cam.camera_open()      #打开摄像头
   
    #发出哔哔哔作为开机声音
    myBeep.beep(3,0.1)

    while True:
         if cam.frame is not None:
            frame = cam.frame.copy()                
            frame = car_tracking(frame,'black')
            #根据得到的坐标画出蓝线，方便看出偏差
            cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
            #如果按了ESC就退出
            cv2.imshow('frame',frame)
            if cv2.waitKey(5) & 0xFF == 27:             
                break
    myUart.uart_send_str('{#000P1500T1000!#001P2100T1000!#002P2300T1000!#003P1000T1000!#004P1500T1000!#005P1500T1000!#006P1500T1000!#007P1500T1000!#008P1500T1000!#009P1500T1000!}')
    cam.camera_close()
    cv2.destroyAllWindows()
