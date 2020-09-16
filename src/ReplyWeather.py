#-*- coding:utf-8 -*-
#和风天气模块，通过API获取实时天气，通过正则检查输入参数
from src.ReplyTryRun import TryRun
from src import GlobalSet

@TryRun
def Weather(name):
    from re import compile
    from requests import get
    from json import loads,dumps
    from os import listdir,mkdir
    from time import time

    Re=compile(r'[^\u4e00-\u9fa5]+')
    KEY='这里是API KEY，请替换为你自己的'

    if Re.search(name):
        return '参数错误，仅支持中文名称'

    #读取缓存
    if 'LocID' not in dir(GlobalSet):
        if 'Cache' not in listdir('src'):
            mkdir('src/Cahce')
        if 'weaChe' not in listdir('src/Cache'):
            mkdir('src/Cache/weaChe')
        if 'LocID' in listdir('src/Cache/weaChe'):
            with open('src/Cache/weaChe/LocID','r') as f:
                GlobalSet.LocID=loads(f.read())
        else:
            GlobalSet.LocID={}
    
    if 'GetTime' not in dir(GlobalSet):
        GlobalSet.GetTime={}
    
    if name not in GlobalSet.LocID:
        a=get('https://geoapi.heweather.net/v2/city/lookup?location='+name+'&key='+KEY)
        Dict=loads(a.text)
        if Dict['status']!='200':
            return '未查询到此地区，请检查名称'
        GlobalSet.LocID[name]=Dict['location'][0]['id']
        with open('src/Cache/weaChe/LocID','w') as f:
            f.write(dumps(GlobalSet.LocID))

    if name not in GlobalSet.GetTime or time()-GlobalSet.GetTime[name]>1800:
        ID=GlobalSet.LocID[name]
        a=get('https://devapi.heweather.net/v7/weather/now?location='+ID+'&key='+KEY)
        Dict=loads(a.text)
        if Dict['code']!='200':
            return '状态码错误，查询失败'
        with open('src/Cache/weaChe/'+ID,'w') as f:
            f.write(a.text)
    else:
        ID=GlobalSet.LocID[name]
        with open('src/Cache/weaChe/'+ID,'r') as f:
            Dict=loads(f.read())
        
    temp=str(Dict['now']['temp'])
    feellike=str(Dict['now']['feelsLike'])
    text=Dict['now']['text']
    Text='查询地区: '+name+'\n实时温度: '+temp+'\n体感温度: '+feellike+'\n天气状况: '+text
    if text=='晴':
        Text=Text+'\n注意遮阳哦!'
    elif text=='雨':
        Text=Text+'\n出门记得带伞哦!'
    elif text=='雪':
        Text=Text+'\n不如叫ta出来一起看雪吧'
    GlobalSet.GetTime[name]=time()
    return Text
