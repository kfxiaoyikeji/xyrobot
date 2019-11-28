# -*- coding: utf-8 -*-
import os
import time
from threading import Thread

def instructionsFunc(text,record,pixels):
    result = False
    isQuit = False
    if (u'退下') in text or (u'跪安') in text:
        os.system("sudo mpg123 staticData/sysvoices/sysvoice6.mp3")
        #record.speech('那我退下了，拜拜')
        pixels.off()
        result = True
        isQuit = True
    
    if (u'开风扇') in text:
        os.system("sudo mpg123 turnon.mp3")
        result = True


    if (u'快一点') in text: 
        os.system("sudo mpg123 faster.mp3")
        result = True

                
    if (u'慢一点') in text:
        os.system("sudo mpg123 lower.mp3")
        result = True


    if (u'关风扇') in text:
        os.system("sudo mpg123 off.mp3")
        result = True
        
    return {'result':result,'isQuit':isQuit}
        
# 自定义线程函数。
def jikeThread(name="jikeThread",record=None,pixels=None):
     while True:
         #开始录音
         pixels.think()
         outputtext = record.record()
         result = instructionsFunc(outputtext,record,pixels)
         if result['isQuit']:
             break;
             
'''
# 创建线程01，不指定参数
thread_01 = Thread(target=main)
# 启动线程01
thread_01.start()

# 创建线程02，指定参数，注意逗号
thread_02 = Thread(target=main, args=("MING",))
# 启动线程02
thread_02.start()
'''