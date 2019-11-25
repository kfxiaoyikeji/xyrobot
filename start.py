# -*- coding: utf-8 -*-
import time
from common import config, constants
from commponents.led import led_Controller as led

class XYRobot(object):
    def init(self):
        print('''
********************************************************
*               xiaoyi-robot - 智能语音机器人            *
*          (c) 2019 Yi.Ma <findlymw@gmail.com>         *
*                     此项目暂时不开源                    *
********************************************************              
              ''')
        config.init()
        
    def run(self):
        self.init()
        
if __name__ == '__main__':
    xyRobot = XYRobot()
    xyRobot.run()
    print(config.get('xyrobot_name'))

    led.wakeup()
    time.sleep(3)
    led.off()