# -*- coding: utf-8 -*-
import os
import apa102
import time
import threading
from gpiozero import LED
#使用队列对led灯进行控制，当发生唤醒后，按照队列的方式进行播放，从而避免控制冲突
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

#引入两个LED灯的播放式样，推荐使用googlehome，比较漂亮
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern

class Pixels:
    #这里定义的是LED灯的数量，这个mic有12个led可以进行控制
    PIXELS_N = 12
    #这里是构造器，参数pattern采用googlehome的样式进行配置
    def __init__(self, pattern=GoogleHomeLedPattern):
        self.pattern = pattern(show=self.show)
        #这个是驱动程序，apa102为led的驱动程序
        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        #配置led灯的引脚号，这里是5,不可改变
        self.power = LED(5)
        self.power.on()
        self.queue = Queue.Queue()
        #创建一个线程
        #target为需要线程去执行的方法名
        #args参数为线程执行方法接收的参数，该属性是一个元组，如果只有一个参数也需要在末尾加
        #逗号
        self.thread = threading.Thread(target=self._run)
        #开启线程的守护进程，设置为True
        self.thread.daemon = True
        #启动这个线程
        self.thread.start()
        #这里记录最后一次的方位，这个4mic通过这个参数定位声音来源的方位
        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    def speak(self,voice):
        self.put(self.pattern.speak)
        os.system("sudo mpg123 "+voice)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()
        
    def positionToDirection(self):
        if self.last_direction != None:
            position = self.last_direction
            print(position)
            '''
            if (position >= 337.5 and position <= 360) or (position >= 0 and position <= 22.5) :
                return 'b' #正后方
            if (position > 22.5 and position <= 67.5):
                return 'lb'#左后方
            if (position > 67.5 and position <= 112.5):
                return 'l'#正左方
            if (position > 112.5 and position <= 157.5):
                return 'lf'#左前方
            if (position > 157.5 and position <= 202.5):
                return 'f'#正前方
            if (position > 202.5 and position <= 247.5):
                return 'rf'#右前方
            if (position > 247.5 and position <= 292.5):
                return 'r'#正右方
            if (position > 292.5 and position < 337.5):
                return 'rb'#右后方
            '''
            
            if (position >= 337.5 and position <= 360) or (position >= 0 and position <= 22.5) :
                return '正后方' #正后方
            if (position > 22.5 and position <= 67.5):
                return '左后方'#左后方
            if (position > 67.5 and position <= 112.5):
                return '正左方'#正左方
            if (position > 112.5 and position <= 157.5):
                return '左前方'#左前方
            if (position > 157.5 and position <= 202.5):
                return '正前方'#正前方
            if (position > 202.5 and position <= 247.5):
                return '右前方'#右前方
            if (position > 247.5 and position <= 292.5):
                return '正右方'#正右方
            if (position > 292.5 and position < 337.5):
                return '右后方'#右后方
        else:
            return ''
        
        


pixels = Pixels()


if __name__ == '__main__':
    while True:

        try:
            pixels.wakeup()
            print('被唤醒。。。')
            time.sleep(3)
            pixels.think()
            print('在思考。。。')
            time.sleep(3)
            pixels.speak()
            print('被讲话。。。')
            time.sleep(6)
            pixels.off()
            print('关掉led。。。')
            time.sleep(3)
        except KeyboardInterrupt:
            break


    pixels.off()
    time.sleep(1)
