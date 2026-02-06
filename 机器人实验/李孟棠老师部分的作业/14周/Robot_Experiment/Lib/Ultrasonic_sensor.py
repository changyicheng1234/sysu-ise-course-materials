#导入模块
import time
import RPi.GPIO as GPIO

#端口模式设置
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#初始化超声波    
def setup_sensor(TRIG_PIN,ECHO_PIN):
    global TRIG,ECHO
    TRIG = TRIG_PIN
    ECHO = ECHO_PIN
    
    GPIO.setup(TRIG, GPIO.OUT,initial = 0)
    GPIO.setup(ECHO, GPIO.IN,pull_up_down = GPIO.PUD_UP)
 
#超声波传感器数据    
def during_time():
    global TRIG,ECHO
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    
   
    while GPIO.input(ECHO) == 0:
        a = 0
          
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
       
    time2 = time.time()
    #返回高电平时间
    during = time2 - time1
    return during
#
def loop_get_data():
    during = during_time()    
    print('during:',during)
    time.sleep(0.1)

#大循环
if __name__ == '__main__':    
    setup_sensor(23,22)       #初始化超声波     
    try:
        while True:
            loop_get_data()
    except KeyboardInterrupt:
        destory()

