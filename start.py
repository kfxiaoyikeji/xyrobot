# -*- coding: utf-8 -*-
import time
from common import config, constants
#导入pixel_ring库，用于配置brightness
from pixel_ring import pixel_ring
#导入gpiozero，控制led
from gpiozero import LED

class XYRobot(object):
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
    
    def __init__(self):
        print('''
********************************************************
*               xiaoyi-robot - 智能语音机器人            *
*          (c) 2019 Yi.Ma <findlymw@gmail.com>         *
*                     此项目暂时不开源                    *
********************************************************              
              ''')
        config.init()       
if __name__ == '__main__':
    xyRobot = XYRobot()
    print(config.get('xyrobot_name'))
    pixel_ring.wakeup()
    time.sleep(2)
    xyRobot.power.off()