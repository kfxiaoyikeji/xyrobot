#coding:utf-8
import time
from aip.speech import AipSpeech
import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(os.path.join(BASE_DIR,'../'))
#print(sys.path)
from common import config

APP_ID = config.get('/baidu_yuyin/appid','17127791')
API_KEY = config.get('/baidu_yuyin/api_key','UY5hD5DgwnPB9DPPVVkjGenN')
SECRET_KEY = config.get('/baidu_yuyin/secret_key','wxhyyGEpTtajKLDOuTUUBAUopTzqEkSp')


aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#string = '现在温度是{}摄氏度'.format(27.0)
strings = [' 好的主人，马上为您开块一点',
          ' 来啦',' 来咯',' 我在呢',' 我在',' 在呢',' 好的',' 欧克','想我了?'
          ]
i = 0
print('per:'+str(config.get('/baidu_yuyin/per')))
for _str in strings:
    result  = aipSpeech.synthesis(_str, 'zh', 1, {
        'vol': 5, 'per': config.get('/baidu_yuyin/per',0),
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        fileName = 'staticData/sysvoices/sysvoice'+str(i)+'.mp3'
        with open(fileName, 'wb') as f:
            f.write(result)
        os.system('mpg123 '+fileName)
    i = i + 1
    time.sleep(1)

