import sys
sys.path.append('/home/pi/Desktop/Robot_Experiment/Lib/')
import time
import UartServer
import Beep 

if __name__ == '__main__':
    UartServer.setup_uart(115200) #设置串口
    Beep.setup_beep()
    #初始化机械臂位置
    UartServer.uart_send_str("#000P1500T1000!#001P2200T1000!#002P2350T1000!#003P1000T1000!#004P1500T1000!#005P1500T1000!")
    time.sleep(2)
    Beep.beep(3,0.1)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        destory() 