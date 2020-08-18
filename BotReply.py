#!/usr/bin/python3
#-*- coding:utf-8 -*-

#这里是引用区
from traceback import format_exc
from src.ReplySendMsg import SendMsg
from src.ReplyAccess import Access
from src.ReplyWeather import Weather
from src.ReplyTryRun import TryRun
from src.ReplyDownload import Download
from src.ReplyJudge import Judge
from src.ReplySetu import Setu
from src.ReplyGege import Gege
from src import GlobalSet
from src.ReplyNoTalk import NoTalk
from src.ReplyTrans import Trans
from src.ReplyPicMark import PicMark
from src.ReplyZhaoXin import ZhaoXin

from requests import get,post
from json import loads,dumps
from sys import exit
import asyncio
import websockets
from time import sleep
from copy import deepcopy
from random import randint

#这里是全局变量定义区
global sessionKey,Setting,Admin,Locache,AdminQQ,LastMsg



#这里是函数定义区

def CheckSocket():
    #检查websocket
    URL='http://0.0.0.0:8080'
    global sessionKey
    a=get(URL+'/config?sessionKey='+sessionKey)
    if loads(a.text)['enableWebsocket']:
        print('Websocket监听已开启')
    else:
        a=post(URL+'/config',dumps({
            'sessionKey':GlobalSet.sessionKey,
            'enableWebsocket':True
            }))
        print('Websocket:\n',a.text)
        if loads(a.text)['msg']=='success':
            print('Websocket监听已开启')
        else:
            exit('开启Websocket失败，退出')

def Auth():
    #认证激活sessionKey
    URL='http://0.0.0.0:8080'
    global sessionKey,AdminQQ
    QQnum=input('机器人QQ号(若为空则使用上次配置):')
    AdminQQ=input('超级管理员QQ(若为空则使用上次配置):')
    sessionKey=input('sessionKey(若为空则优先读取记录,无记录自动获取)\n输入new获取新Key:')
    try:
        with open('src/Cache/QQ','r') as f:
            QQList=loads(f.read())
        if 'QQnum' not in QQList:
            QQnum=input('无记录,请输入机器人QQ:')
            QQList['QQnum']=QQnum
        else:
            if not QQnum:
                QQnum=QQList['QQnum']
        if 'AdminQQ' not in QQList:
            AdminQQ=input('无记录,请输入超级管理员QQ:')
            QQListp['AdminQQ']=AdminQQ
        else:
            if not AdminQQ:
                AdminQQ=QQList['AdminQQ']
        if 'sessionKey' in QQList and sessionKey!='new':
            sessionKey=QQList['sessionKey']
        
        with open('src/Cache/QQ','w') as f:
            f.write(dumps(QQList))
    except Exception:
        QQList={}
        QQnum=input('无记录,请输入机器人QQ:')
        AdminQQ=input('无记录,请输入超级管理员QQ:')
        QQList['QQnum']=QQnum;QQList['AdminQQ']=AdminQQ
    if not sessionKey or sessionKey=='new':
        authKey=input('authKey:')
        a=post(URL+'/auth',dumps({'authKey':authKey}))
        sessionKey=loads(a.text)['session']
        GlobalSet.sessionKey=sessionKey
        print('sessionKey:',sessionKey)
        a=post(URL+'/verify',dumps({
            'sessionKey':sessionKey,
            'qq':QQnum
            }))
        print('校验session:\n',a.text)
    GlobalSet.sessionKey=sessionKey
    QQList['sessionKey']=sessionKey
    QQList['AdminQQ']=AdminQQ
    QQList['QQnum']=QQnum
    with open('src/Cache/QQ','w') as f:
        f.write(dumps(QQList))
    print('AdminQQ:',AdminQQ)
    print('sessionKey:',GlobalSet.sessionKey)


async def run():
    #监听消息函数
    global sessionKey
    url='ws://0.0.0.0:8080/all?sessionKey='+sessionKey
    async with websockets.connect(url) as websocket:
        while True:
            msg=await websocket.recv()
            dmsg=loads(msg)
            print(dmsg)
            Reply(dmsg)

@TryRun
def Reply(dmsg):
    global Setting,AdminQQ
    if dmsg['type']=='FriendMessage':
        target=dmsg['sender']['id']
        
        #Weather
        if Judge(dmsg,KeyWords=['#天气']):
            LocName=dmsg['messageChain'][1]['text'].split()[1]
            SendMsg(target,'Friend',Text=Weather(LocName))
            sleep(0.3)
            #FLAG,待更改
            SendMsg(target,'Friend',ImageUrl='http://127.0.0.1:35678/botpic/biu.jpg')
            return 0
        
        #小哥哥
        if Judge(dmsg,ReWords=r'来点[\s\S]*好看[\s\S]*的'):
            text=Gege(target)
            if text!=0:
                SendMsg(target,'Friend',Text=str(text))
            return 0
        #百度翻译
        if Judge(dmsg,KeyWords=['wd']):
            SendMsg(target,'Friend',Text=Trans(dmsg))
            return 0
        
        SendMsg(target,'Friend',Text='Hi!\n我是小pi,基于mirai的QQ机器人\n更多功能正在开发中')

    elif dmsg['type']=='TempMessage':
        SenderID=dmsg['sender']['id']
        target=dmsg['sender']['group']['id']
        
        #Weather
        if Judge(dmsg,KeyWords=['#天气']):
            LocName=dmsg['messageChain'][1]['text'].split()[1]
            SendMsg(target,'Temp',SenderID=SenderID,Text=Weather(LocName))
            sleep(0.3)
            #FLAG,待更改
            SendMsg(target,'Temp',SenderID=SenderID,ImageUrl='http://127.0.0.1:35678/botpic/biu.jpg')
            return 0

        SendMsg(target,'Temp',SenderID=SenderID,Text='Hi!\n我是小pi,基于mirai的QQ机器人\n更多功能正在开发中')

    elif dmsg['type']=='GroupMessage':
        target=dmsg['sender']['group']['id']
        SenderID=str(dmsg['sender']['id'])
        print('\ntarget:',target,'\nsender:',SenderID,'\n')
        #不同权限可使用功能不同
        if SenderID==AdminQQ:
            flag=3
        elif Access(SenderID,mode='check'):
            flag=2
        else:
            flag=1

        #超级管理员
        if flag>2: 
            if Judge(dmsg,KeyWords=['#op']) and Judge(dmsg,Type='At'):
                if dmsg['messageChain'][1]['type']=='At':
                    SendMsg(target,'Group',Text=Access(dmsg['messageChain'][1]['target'],mode='set',status=True))
                    return 0
            if Judge(dmsg,KeyWords=['#rmop']) and Judge(dmsg,Type='At'):
                if dmsg['messageChain'][1]['type']=='At':
                    SendMsg(target,'Group',Text=Access(dmsg['messageChain'][1]['target'],mode='set',status=False))
                    return 0
        
        #管理员
        if flag>1:
            #开关机器人
            if Judge(dmsg,KeyWords=['#set']):
                if Judge(dmsg,KeyWords=['#set','open']):
                    SendMsg(target,'Group',Text=Access(target,App='Open',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','close']):
                    SendMsg(target,'Group',Text=Access(target,App='Open',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Setu','close']):
                    SendMsg(target,'Group',Text=Access(target,App='Setu',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Setu','open']):
                    SendMsg(target,'Group',Text=Access(target,App='Setu',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Zhaoxin','open']):
                    SendMsg(target,'Group',Text=Access(target,App='Zhaoxin',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Zhaoxin','close']):
                    SendMsg(target,'Group',Text=Access(target,App='Zhaoxin',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Gege','open']):
                    SendMsg(target,'Group',Text=Access(target,App='Gege',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Gege','close']):
                    SendMsg(target,'Group',Text=Access(target,App='Gege',mode='set',status=False))
                    return 0
            #群禁烟
            if Judge(dmsg,Type='At'):
                if Judge(dmsg,ReWords=r'上一[\s\S]*杯[\s\S]*茶'):
                    target=dmsg['sender']['group']['id']
                    SendMsg(target,'Group',Text=NoTalk(dmsg))
                    return 0
               