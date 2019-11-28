# -*- coding: utf-8 -*-
import time
import os
import random
import signal,sys
from threading import Thread
from common import config, constants
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA
from commponents.kws.pixels import pixels

from commponents.baidu_STT import record
from commponents.instructions import instructions

# Base64编码是一种“防君子不防小人”的编码方式 生成的编码可逆，后一两位可能有“=”，生成的编码都是ascii字符
import base64
# requests库是一个常用的用于http请求的模块，它使用python语言编写，可以方便的对网页进行爬取，是学习python爬虫的较好的http请求模块。
import requests

class XYRobot(object):
    
    jike = config.get('jike',False)
    
    src = Source(rate=16000, channels=4, frames_size=320)
    ch1 = ChannelPicker(channels=4, pick=1)
    #这里需要填写pmdl的绝对路径
    #kws = KWS()
    #kws = KWS(os.path.join(constants.DATA_PATH ,config.get('kws_file_name','')))
    kws = KWS(os.path.join(constants.DATA_PATH ,config.get('kws_file_name','')))
    doa = DOA(rate=16000)
    
    def __init__(self):
        print('极客模式:'+str(self.jike))
        self.src.link(self.ch1)
        self.ch1.link(self.kws)
        self.src.link(self.doa)
        def on_detected(keyword):
            position = self.doa.get_direction()
            pixels.wakeup(position)
            voice = os.path.join(constants.DATA_PATH,'sysvoices','sysvoice'+str(random.randint(1,8))+'.mp3')
            direction = pixels.positionToDirection()
            print('detected {} at direction {} is {}'.format(keyword, position,direction))
            #这里是唤醒后进行打招呼的语音播放
            pixels.speak(voice)
            print(str(keyword)+voice)
            
            record.speech('你在我'+direction)
            
            if self.jike:
                print('进入极客模式')
                # 创建线程01，不指定参数
                thread_01 = Thread(target=instructions.jikeThread, args=("jikeThread01",record,pixels,))
                # 启动线程01
                thread_01.start()
            else:
                #开始录音
                outputtext = record.record()
                #这里是指令，语音识别后返回文字，将文字传入instructionsFunc，进行处理和播放
                instructions.instructionsFunc(outputtext,record,pixels)
            
            
        self.kws.set_callback(on_detected)
        self.src.recursive_start()
            
        config.init()
        
        
    def sigint_handler(self,signum, frame):
        record.stream.stop_stream()
        record.stream.close()
        record.p.terminate()
        
        self.src.recursive_stop()
        
        print 'catched interrupt signal!'
        sys.exit(0)
        
    def train(self, w1, w2, w3, m):
            '''
            传入三个wav文件，生成snowboy的.pmdl模型
            '''
            def get_wave(fname):
                with open(fname, 'rb') as infile:
                    return base64.b64encode(infile.read()).decode('utf-8')
            url = 'https://snowboy.kitt.ai/api/v1/train/'
            data = {
                "name": "wukong-robot",
                "language": "zh",
                "token": config.get('snowboy_token', ''),
                "voice_samples": [
                    {"wave": get_wave(w1)},
                    {"wave": get_wave(w2)},
                    {"wave": get_wave(w3)}
                ]
            }
            
            response = requests.post(url, json=data)
            print(response.ok)
            if response.ok:
                with open(m, "wb") as outfile:
                    outfile.write(response.content)
                return 'Snowboy模型已保存至{}'.format(m)
            else:
                return "Snowboy模型生成失败，原因:{}".format(response.text)
        
if __name__ == '__main__':
    print('''
********************************************************
*               xiaoyi-robot - 智能语音机器人            *
*          (c) 2019 Yi.Ma <findlymw@gmail.com>         *
*                     此项目暂时不开源                    *
********************************************************              
              ''')
    xyRobot = XYRobot()
    # 注册ctrl-c中断
    signal.signal(signal.SIGINT, xyRobot.sigint_handler)
    
    '''
    xyRobot.train('/home/pi/Documents/workspace/xyrobot/staticData/ellaella0.wav','/home/pi/Documents/workspace/xyrobot/staticData/ellaella1.wav','/home/pi/Documents/workspace/xyrobot/staticData/ellaella2.wav','/home/pi/Documents/workspace/xyrobot/staticData/ellaella.pmdl')
    '''
    
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    xyRobot.sigint_handler()