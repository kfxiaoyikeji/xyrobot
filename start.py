# -*- coding: utf-8 -*-
import time
from common import config, constants
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA
from commponents.kws.pixels import pixels

class XYRobot(object):
    src = Source(rate=16000, channels=4, frames_size=320)
    ch1 = ChannelPicker(channels=4, pick=1)
    kws = KWS()
    doa = DOA(rate=16000)
    
    def __init__(self):
        self.src.link(self.ch1)
        self.ch1.link(self.kws)
        self.src.link(self.doa)
        def on_detected(keyword):
            position = self.doa.get_direction()
            pixels.wakeup(position)
            direction = pixels.positionToDirection()
            self.kws.set_callback(on_detected)
            
            print('detected {} at direction {} is {}'.format(keyword, position,direction))
        self.kws.set_callback(on_detected)
        self.src.recursive_start()
    
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
    
        self.src.recursive_stop()
        
        config.init()       
if __name__ == '__main__':
    print('''
********************************************************
*               xiaoyi-robot - 智能语音机器人            *
*          (c) 2019 Yi.Ma <findlymw@gmail.com>         *
*                     此项目暂时不开源                    *
********************************************************              
              ''')
    print(config.get('xyrobot_name'))
    xyRobot = XYRobot()