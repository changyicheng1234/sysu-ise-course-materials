#导包
import RPi.GPIO as GPIO
import time

#端口模式设置
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#引脚定义
LED_PIN = 4

systick_ms_led = 0

#点亮LED 参数led_pin 为引脚编号
def on():
    GPIO.output(LED_PIN, 0)

#熄灭LED 参数led_pin 为引脚编号
def off():
    GPIO.output(LED_PIN, 1)

#反转LED 参数led_pin 为引脚编号
def flip():
    GPIO.output(LED_PIN, not GPIO.input(LED_PIN))
    
#初始化LED灯
def setup_led():
    GPIO.setup(LED_PIN, GPIO.OUT)


#大循环LED灯
def loop_led():
    global systick_ms_led
    if(int((time.time() * 1000))- systick_ms_led > 500):
        systick_ms_led = int((time.time() * 1000))
        flip()

#程序反复执行处
if __name__ == "__main__":
    setup_led()
    try:
        while True:
            loop_led()
    except KeyboardInterrupt:
        off()
