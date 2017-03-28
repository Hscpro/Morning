# -*- coding: utf-8 -*-
import os
import urllib
import urllib2,json
from datetime import date
from os import path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_city_id(cityname, search_type=1):
    ids = ''
    if search_type == 1:# 查询城市ID
        search = 'allchina'
        fn0 = 'cityID'
    elif search_type == 0:# 查询景点ID
        fn0 = 'viewID'
        search = 'allattractions'
    else:
        # 代表type值出错
        return -1
    fn = fn0+str(date.today())+'.txt'
    try:
        if path.exists(fn):
            fp = open(fn, 'r')
            context = fp.read()
            fp.close()
        else:
            fp = open(fn, 'w')
            url_city = 'https://free-api.heweather.com/v5/citylist?search='+search+'&key=和风天气KEY'
            req = urllib2.Request(url_city)
            resp = urllib2.urlopen(req)
            context = resp.read().decode('utf-8')
            # print True
            fp.write(context)
            fp.close()
        city_json = json.loads(context,encoding='utf-8')
        city_info = city_json["city_info"]
        city_name = unicode(cityname, 'utf-8')
        # print city_name
        for index, cities in enumerate(city_info):
            if city_name in cities['city']:
                print cities['city']
                ids = cities['id']
                break
        else:
            # 之后将会返回-1
            print '您输入的城市或景点不存在，请反馈给管理员'
    except IOError, e:
        print e
    else:
        pass
    return ids


#返回和风天气数据
def get_city_weather(index, search_type=1):
    if search_type == 1:
        search = 'weather'
    elif search_type == 0:
        search = 'attractions'
    else:
        return -1
    url_weather = 'https://free-api.heweather.com/v5/'+search+'?city='+index+'&key=和风天气KEY'
    req = urllib2.Request(url_weather)
    resp = urllib2.urlopen(req)
    context = resp.read()
    weather_json = json.loads(context, encoding='utf-8')
    fp = open("/home/Morning/temp/test.txt", 'w')
    fp.write(context)
    fp.close()
    if search_type == 1:
        weather = weather_json["HeWeather5"][0]['daily_forecast'][0]
    else:
        weather = weather_json
    return weather


#获取百度语音token
def get_token():
    api_key = "百度语音api_key"
    sec_key = "百度语音sec_key"
    url = url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+sec_key
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    context = resp.read().decode('utf-8')
    return json.loads(context)['access_token']


#获取需要的数据
def get_wat():
    city_id = "CN101280601"  #城市代码   
    city_weather = get_city_weather(city_id)
    a= city_weather['tmp']['max']
    b= city_weather['tmp']['min']
    c= city_weather['cond']['txt_d']
    d= city_weather['cond']['txt_n']
    e= city_weather['date']
    return "早上好,今天是{},最高温度{}度,最低温度{}度,日间天气{},夜间天气{}.".format(e,a,b,c,d)

token=get_token()
weather=get_wat()

#tts
url = "http://tsn.baidu.com/text2audio?tex="+weather+"&lan=zh&per=3&pit=5&spd=5&cuid=b827ebcac3a8&ctp=1&tok="+token
#url = "http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=5&text=" + weather

#播放
try:
	os.system('/home/Morning/vlc/volume-drop.sh')
	os.system('/usr/bin/mplayer -cache-min 80 -volume 40 "%s"' %(url))
	os.system('/home/Morning/vlc/volume-rise.sh')

except Exception as e:
    print('Exception',e)