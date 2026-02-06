from math import *
import sys
sys.path.append('/home/pi/Desktop/Robot_Experiment/Lib/')
import time
import UartServer
import Beep

pi = 3.1415926


servo_angle = [0,0,0,0]#记录角度
servo_pwm = [0,0,0,0]#记录pwm

'''

设置四个关节的长度
单位0.1mm
l0  底盘到第二个舵机中心轴的距离
l1  第二个舵机到第三 个舵机的距离
l2  第三个舵机到第四 个舵机的距离
l3  第四个舵机到机械臂(闭合后)最高点的距离

'''
def setup_kinematics(L0, L1, L2, L3) :
    global l0, l1 ,l2 ,l3
    #放大10倍
    l0 = L0*10
    l1 = L1*10
    l2 = L2*10
    l3 = L3*10

'''
    x,y 为映射到平面的坐标
    z为距离地面的距离
    Alpha 为爪子和平面的夹角 -25~-65范围比较好
'''
#x,y,z为爪子闭合时的末端点的坐标，alpha为爪子与水平面的角度
def kinematics_analysis(x, y, z, Alpha):
    global pi,l0, l1 ,l2 ,l3,servo_angle,servo_pwm
   
    #放大10倍
    x = x*10
    y = y*10
    z = z*10
    
   
    if(x == 0 and y != 0) :
        theta6 = 0.0
    elif(x > 0 and y == 0):
        theta6 = 90
    elif(x < 0 and y == 0):
        theta6 = -90
    else :
        theta6 = atan(x/y)*180.0/pi #计算云台旋转角度
    
    '''   
    #已知x y 坐标，求解x，y的斜边q 
    #求y1+y2
    #求z1+z2
    '''
    
    if(z < -l0) :
        return 1;
    if(sqrt(y*y + z*z) > (l1+l2)) :
        return 2
    
    '''
    #计算l_2末端与0点连线的水平夹角和l_2末端与0点连线的l_1夹角
    c=?
    b=?
    '''
    
    if (z < 0) :
        zf_flag = -1
    else :
        zf_flag = 1
    
    theta1 = c * zf_flag + acos(b);     #计算1号舵机的弧度
    theta1 = theta1 * 180.0 / pi;           #转化为角度 
    if(theta1 > 180.0 or theta1 < 0.0) :
        return 4
    
    #根据公式计算2号舵机的弧度，再转化为角度
    '''
    公式补充部分
    '''

    if (theta2 > 135.0 or theta2 < -135.0) :    #判断是否越界
        return 6
    

    #根据公式计算2号舵机的弧度，再转化为角度
    '''
    公式补充部分
    '''
    if(theta3 > 90.0 or theta3 < -90.0) :
        return 7
    
    
    servo_angle[0] = theta6
    servo_angle[1] = theta1-90
    servo_angle[2] = theta2
    servo_angle[3] = theta3    
    
    servo_pwm[0] = (int)(1500-2000.0 * servo_angle[0] / 270.0);
    servo_pwm[1] = (int)(1500+2000.0 * servo_angle[1] / 270.0);
    servo_pwm[2] = (int)(1500+2000.0 * servo_angle[2] / 270.0);
    servo_pwm[3] = (int)(1500+2000.0 * servo_angle[3] / 270.0);
    
    return 0;

#此函数可移植到要执行的主程序里面去
def kinematics_move(x,y,z,mytime): 
    global servo_pwm
    alpha_list = []
    if(y < 0):
        return 0;
    #寻找3号舵机的最佳角度
    flag = 0;
    best_alpha = 0
    for i in range(-25,-65,-1) :
        if kinematics_analysis(x,y,z,i):
            alpha_list.append(i)
    if len(alpha_list) > 0:
        if y > 2150:
            best_alpha = max(alpha_list)
        else:
            best_alpha = min(alpha_list)
        flag = 1
        
    #用3号舵机与水平最大的夹角作为最佳值
    if(flag) :
        kinematics_analysis(x,y,z,best_alpha);
        testStr = '{'
        for j in range(0,4) :
            #set_servo(j, servo_pwm[j], time);
            #print(servo_pwm[j])
            testStr += "#%03dP%04dT%04d!" % (j,servo_pwm[j],mytime)
        testStr += '}'
        print(testStr)
        myUart.uart_send_str(testStr)
        return 1
    
    return 0