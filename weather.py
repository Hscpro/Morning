# -*- coding: utf-8 -*-
import os
import urllib
import urllib2,json
from datetime import date
from os import path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#返回和风天气数据
def get_city_weather(index, search_type=1):
    if search_type == 1:
        search = 'weather'
    elif search_type == 0:
        search = 'attractions'
    else:
        return -1
    url_weather = 'https://free-api.heweather.com/s6/weather/forecast?location='+index+'&key=aaaaaxxxxxdsdd23423cvdfd'
    req = urllib2.Request(url_weather)
    resp = urllib2.urlopen(req)
    context = resp.read()
    weather_json = json.loads(context, encoding='utf-8')
    fp = open("/home/pi/private/Morning/temp/test.txt", 'w')
    fp.write(context)
    fp.close()
    if search_type == 1:
        weather = weather_json["HeWeather6"][0]['daily_forecast'][0]
    else:
        weather = weather_json
    return weather


#获取百度语音token
def get_token():
    api_key = "百度语音api_key"
    sec_key = "百度语音sec_key"
    url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+sec_key
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    context = resp.read().decode('utf-8')
    return json.loads(context)['access_token']


#获取需要的数据
def get_wat():
    city_id = "CN101110101"  #城市代码   
    city_weather = get_city_weather(city_id)
    a= city_weather['date']
    b= city_weather['tmp_max']
    c= city_weather['tmp_min']
    d= city_weather['cond_txt_d']
    e= city_weather['cond_txt_n']
    print("早上好,今天是{},最高温度{}度,最低温度{}度,日间天气{},夜间天气{}.".format(a,b,c,d,e))
    return "早上好,今天是{},最高温度{}度,最低温度{}度,日间天气{},夜间天气{}.".format(a,b,c,d,e)

token=get_token()
weather=get_wat()

#tts
url = "http://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=abcdxxx&tok="+token+"&tex="+weather+"&vol=9"
#url = "http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=5&text=" + weather

#播放
try:
    os.system('/home/pi/private/Morning/vlc/volume-drop.sh')
    os.system('/usr/bin/mplayer -cache-min 80  -volume 240 "%s"' %(url))
    os.system('/home/pi/private/Morning/vlc/volume-rise.sh')

except Exception as e:
    print('Exception',e)
