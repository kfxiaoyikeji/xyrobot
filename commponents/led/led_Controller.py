# -*- coding: utf-8 -*-

"""
Control pixel ring on ReSpeaker 4 Mic Array

pip install pixel_ring gpiozero
"""
#使用time库使用sleep方法
import time
#导入pixel_ring库，用于配置brightness
from pixel_ring import pixel_ring
#导入gpiozero，控制led
from gpiozero import LED
#LED（5）代表了使用的是5的引脚，5的引脚为正极
power = LED(5)
#打开led灯
power.on()

# 设置led的亮度，取值范围为1-100的整数
pixel_ring.set_brightness(10)

# 设置led的wakeup、think、speak的两等形式
# 设置led的图案样式，可以修改pattern.py，也可以进行更多添加，然后再在apa102_pixel_ring.py中进行添加。
# 默认为googlehome的方式，主要为彩色，echo主要为蓝色
#pixel_ring.change_pattern('echo')

if __name__ == '__main__':
    while True:

        try:
            #唤醒时使用
            pixel_ring.wakeup()
            time.sleep(3)
            #听到声音后想的loading时使用
            pixel_ring.think()
            time.sleep(3)
            #说话的时候使用
            pixel_ring.speak()
            time.sleep(6)
            #关闭led灯
            pixel_ring.off()
            time.sleep(3)
            #googlehome和echo循环展示，生产上只用一个就可以了。建议使用googlehome，漂亮
            pixel_ring.change_pattern('')
        except KeyboardInterrupt:
            break


    pixel_ring.off()
    time.sleep(1)

power.off()
