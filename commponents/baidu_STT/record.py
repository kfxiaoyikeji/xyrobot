# -*- coding: utf-8 -*-
import pyaudio
from baidu_speech_api import BaiduVoiceApi
import json
import sys
import os
from aip.speech import AipSpeech

from urllib2 import Request, urlopen, URLError, HTTPError

BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(os.path.join(BASE_DIR,'../'))
#print(sys.path)
from common import config

APP_ID = config.get('/baidu_yuyin/appid','17127791')
API_KEY = config.get('/baidu_yuyin/api_key','UY5hD5DgwnPB9DPPVVkjGenN')
SECRET_KEY = config.get('/baidu_yuyin/secret_key','wxhyyGEpTtajKLDOuTUUBAUopTzqEkSp')

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1
RESPEAKER_WIDTH = 2
CHUNK = 1024
RECORD_SECONDS = config.get('recording_timeout',3)

p = pyaudio.PyAudio()
stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            start=False,)



aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

baidu = BaiduVoiceApi(appkey=API_KEY,secretkey=SECRET_KEY)

def generator_list(list):
    for l in list:
        yield l

def record():
    stream.start_stream()
    print("* recording")
    frames = []
    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    print("start to send to baidu")
    # audio_data should be raw_data
    text = baidu.server_api(generator_list(frames))
    if text:
        try:
            text = json.loads(text)
            for t in text['result']:
                print(t)
                return(t)
        except KeyError: 
            return("get nothing")
    else:
        print("get nothing")
        return("get nothing")

def sigint_handler(signum, frame):
    stream.stop_stream()
    stream.close()
    p.terminate()
    print 'catched interrupt signal!'
    sys.exit(0)