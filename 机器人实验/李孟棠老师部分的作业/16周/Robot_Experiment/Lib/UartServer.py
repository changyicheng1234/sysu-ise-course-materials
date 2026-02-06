#导包
import Led 
import Beep
import serial
import time
import threading

#全局变量定义
ser = ''
uart_baud = 115200
uart_get_ok = 0
uart_receive_buf = ""
uart_receive_buf_index = 0

#发送字符串 只需传入要发送的字符串即可
def uart_send_str(string):
    global ser
    ser.write(string.encode("utf-8"))
    time.sleep(0.01)
    ser.flushInput()

#线程调用函数，主要处理数据接受格式，主要格式为 $...!   #...! {...}三种格式，...内容长度不限
def serialEvent():
    global ser,uart_receive_buf_index,uart_receive_buf,uart_get_ok
    mode = 0
    try:
        while True:
            if uart_get_ok == 0:
                uart_receive_buf_index = ser.inWaiting()
                if uart_receive_buf_index > 0:
                    uart_receive_buf = uart_receive_buf+ser.read(uart_receive_buf_index).decode("utf-8","ignore")
                    #print('get1:',uart_receive_buf, " len:", len(uart_receive_buf), " mode:", mode)
                    if mode == 0:
                        if uart_receive_buf.find('{') >= 0:
                            mode = 1
                            #print('mode1 start')
                        elif uart_receive_buf.find('$') >= 0:
                            mode = 2
                            #print('mode2 start')
                        elif uart_receive_buf.find('#') >= 0:
                            mode = 3
                            #print('mode3 start')
                    
                    if mode == 1:
                        if uart_receive_buf.find('}') >= 0:
                            uart_get_ok = 1
                            mode = 0
                            ser.flushInput()
                            #print('{}:',uart_receive_buf, " len:", len(uart_receive_buf))
                            #print('mode1 end')
                    elif mode == 2:
                        if uart_receive_buf.find('!') >= 0:
                            uart_get_ok = 2
                            mode = 0
                            ser.flushInput()
                            #print('$!:',uart_receive_buf, " len:", len(uart_receive_buf))
                            #print('mode2 end')
                    elif mode == 3:
                        if uart_receive_buf.find('!') >= 0:
                            uart_get_ok = 3
                            mode = 0
                            ser.flushInput()
                            #print('#!:', uart_receive_buf, " len:", len(uart_receive_buf))
                            #print('mode3 end')
                    
                    #print('get2:',uart_receive_buf, " len:", len(uart_receive_buf), " mode:", mode, " getok:", uart_get_ok)
    
    except IOError:
        pass;

#串口接收线程
uart_thread = threading.Thread(target=serialEvent)

#串口初始化
def setup_uart(baud):
    global ser,uart_thread,uart_receive_buf
    uart_baud = baud
    ser = serial.Serial("/dev/ttyAMA0", uart_baud)
    ser.flushInput()
    uart_thread.start()
    uart_send_str("uart init ok!\r\n");
    uart_receive_buf = ''
        
#大循环
if __name__ == '__main__':
    setup_uart(115200)
    Led.setup_led()
    Beep.setup_beep()
    #发出哔哔哔作为开机声音
    Beep.beep(3,0.1)
   

    try:
        while True:            
            if uart_get_ok:
                print(int(time.time()*1000))
                uart_send_str(uart_receive_buf)
                
                if uart_receive_buf == '$LEDON!':
                    Led.on()
                    uart_send_str("{#000P25001000!#001P1500T1000!}");
                elif uart_receive_buf == '$LEDOFF!':
                    Led.off()
                elif uart_receive_buf == '$BEEPON!':
                    Beep.on()
                elif uart_receive_buf == '$BEEPOFF!':
                    Beep.off()
                
                uart_receive_buf = ''
                uart_get_ok = 0

    except KeyboardInterrupt:
        if ser != None:
            ser.close()
     
