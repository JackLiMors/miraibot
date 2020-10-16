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
from src import GlobalSet
from src.ReplyNoTalk import NoTalk
from src.ReplyZhaoXin import ZhaoXin
from src.ReplyPic import Pic
from src.ReplyCount import Count

from requests import get,post
from json import loads,dumps
from sys import exit
import asyncio
import websockets
from time import sleep
from copy import deepcopy
from random import randint
#from thread

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
    GlobalSet.AdminQQ=AdminQQ


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

#async def TimeSend(

@TryRun
def Reply(dmsg):
    global Setting,AdminQQ
    if len(dmsg)<1:
        return 0
    if dmsg['type']=='FriendMessage':
        target=dmsg['sender']['id']
        
        #Weather
        if Judge(dmsg,KeyWords=['#天气']):
            LocName=dmsg['messageChain'][1]['text'].split()[1]
            SendMsg(target,targetType='Friend',Text=Weather(LocName))
            sleep(0.3)
            #FLAG,待更改
            #SendMsg(target,'Friend',ImageUrl='http://127.0.0.1:30000/botpic/biu.jpg')
            return 0
        
        #小哥哥
        if Judge(dmsg,ReWords=r'来点[\s\S]*好看[\s\S]*的'):
            Pic(target,str(target)+str(target))
            return 0
        
        SendMsg(target,targetType='Friend',Text='Hi!\n我是小pi,基于mirai的QQ机器人\n更多功能正在开发中')

    elif dmsg['type']=='TempMessage':
        SenderID=dmsg['sender']['id']
        target=dmsg['sender']['group']['id']
        
        #Weather
        if Judge(dmsg,KeyWords=['#天气']):
            LocName=dmsg['messageChain'][1]['text'].split()[1]
            SendMsg(target,targetType='Temp',SenderID=SenderID,Text=Weather(LocName))
            sleep(0.3)
            #FLAG,待更改
            #SendMsg(target,targetType'Temp',SenderID=SenderID,ImageUrl='http://127.0.0.1:30000/botpic/biu.jpg')
            return 0

        SendMsg(target,targetType='Temp',SenderID=SenderID,Text='Hi!\n我是小pi,基于mirai的QQ机器人\n更多功能正在开发中')

    elif dmsg['type']=='GroupMessage':
        #记录发言成员
        Count(dmsg)
        target=dmsg['sender']['group']['id']
        SenderID=str(dmsg['sender']['id'])
        print('\ntarget:',target,'\nsender:',SenderID,'\n')
        #不同权限可使用功能不同
        if SenderID==AdminQQ:
            flag=3
        elif Access(SenderID):
            flag=2
        else:
            flag=1

        #超级管理员
        if flag>2: 
            if Judge(dmsg,KeyWords=['#op']) and Judge(dmsg,Type='At'):
                if dmsg['messageChain'][1]['type']=='At':
                    SendMsg(target,Text=Access(dmsg['messageChain'][1]['target'],mode='set',status=True))
                    return 0
            if Judge(dmsg,KeyWords=['#rmop']) and Judge(dmsg,Type='At'):
                if dmsg['messageChain'][1]['type']=='At':
                    SendMsg(target,Text=Access(dmsg['messageChain'][1]['target'],mode='set',status=False))
                    return 0
        
        #管理员
        if flag>1:
            #开关机器人
            if Judge(dmsg,KeyWords=['#set']):
                if Judge(dmsg,KeyWords=['#set','open']):
                    SendMsg(target,Text=Access(target,App='Open',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','close']):
                    SendMsg(target,Text=Access(target,App='Open',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Setu','close']):
                    SendMsg(target,Text=Access(target,App='Setu',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','Setu','open']):
                    SendMsg(target,Text=Access(target,App='Setu',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','ZhaoXin','open']):
                    SendMsg(target,Text=Access(target,App='ZhaoXin',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','ZhaoXin','close']):
                    SendMsg(target,Text=Access(target,App='ZhaoXin',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','status']):
                    SendMsg(target,Text=Access(target,App='1',mode='status'))
                    return 0
                if Judge(dmsg,KeyWords=['#set','TimeSend','close']):
                    SendMsg(target,Text=Access(target,App='TimeSend',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','TimeSend','open']):
                    SendMsg(target,Text=Access(target,App='TimeSend',mode='set',status=True))
                    return 0
                if Judge(dmsg,KeyWords=['#set','NoTalk','close']):
                    SendMsg(target,Text=Access(target,App='NoTalk',mode='set',status=False))
                    return 0
                if Judge(dmsg,KeyWords=['#set','NoTalk','open']):
                    SendMsg(target,Text=Access(target,App='NoTalk',mode='set',status=True))
                    return 0

            #群禁烟
            if Judge(dmsg,Type='At') and Access(target,App='NoTalk'):
                if Judge(dmsg,ReWords=r'上一[\s\S]*杯[\s\S]*茶'):
                    SendMsg(target,Text=NoTalk(dmsg))
                    return 0
                if Judge(dmsg,ReWords=r'上两[\s\S]*杯[\s\S]*茶'):
                    SendMsg(target,Text=NoTalk(dmsg,level=2))
                    return 0
                if Judge(dmsg,ReWords=r'上三[\s\S]*杯[\s\S]*茶'):
                    SendMsg(target,Text=NoTalk(dmsg,level=3))
                    return 0
            #解除禁烟
            if Judge(dmsg,Type='At') and Judge(dmsg,KeyWords=['下茶']) and Access(target,App='NoTalk'):
                SendMsg(target,Text=NoTalk(dmsg,mode='unset'))
                return 0
            #保存涩图
            if Judge(dmsg,Type='Quote') and Judge(dmsg,KeyWords=['#hso']):
                msgID=dmsg['messageChain'][1]['id']
                Pic(target,'setu',msgID=msgID)
                return 0
            #op帮助手册
            if Judge(dmsg,KeyWords=['ophelp']):
                SendMsg(target,Text='Bot op帮助手册:\n\n开启/关闭相应功能:\n\t#set 功能名称 open/close\n\n功能开关状态:\n\t#set status')
                return 0


        #一般功能
        #招新，此函数不使用return 0结束函数，考虑到运行效率，谨慎启用
        if not Access(target,App='Open',mode='check'):
            return 0
        if Access(target,App='ZhaoXin'):
            text=ZhaoXin(dmsg)
            if text:
                SendMsg(target,Text=text)

        #天气
        if Access(target,App='Weather') and Judge(dmsg,KeyWords=['#天气']):
            LocName=dmsg['messageChain'][1]['text'].split()[1]
            SendMsg(target,Text=Weather(LocName))
            sleep(0.3)
            #FLAG,待更改
            #SendMsg(target,ImageUrl='http://127.0.0.1:30000/botpic/biu.jpg')
            return 0
        #Setu
        if Access(target,App='Setu') and Judge(dmsg,ReWords=r'来点[\s\S]*好康[\s\S]*的'):
            if randint(1,25)<3:
                SendMsg(target,ImageID='{0C1CBC41-45C2-1919-58CE-A56AA3A4C578}.mirai')
            else:
                Pic(target,'setu')
            return 0
            #SendMsg(target,Text='功能维护中')
            return 0
        #PSetu
        if Judge(dmsg,ReWords=r'来点[\s\S]*好看[\s\S]*的'):
            Pic(target,SenderID+SenderID)
            return 0
        #Pic
        if Judge(dmsg,KeyWords=['#pic']):
            name=dmsg['messageChain'][-1]['text'].split()
            if len(name)<2:
                SendMsg(target,Text='请指定图片的名称\n格式: #mark 名称')
                return 0
            name=name[1]
            Pic(target,SenderID,name=name)
            return 0
        if Judge(dmsg,Type='Quote'):
            #个人图库
            if Judge(dmsg,KeyWords=['hso']):
                msgID=dmsg['messageChain'][1]['id']
                Pic(target,SenderID+SenderID,msgID=msgID)
                return 0
            #mark
            if Judge(dmsg,KeyWords=['#mark']):
                msgID=dmsg['messageChain'][1]['id']
                name=dmsg['messageChain'][-1]['text'].split()
                if len(name)<2:
                    SendMsg(target,Text='请指定要保存的名称\n格式: #mark 名称')
                    return 0
                name=name[1]
                Pic(target,SenderID,name=name,msgID=msgID)
                return 0
        #帮助手册
        if Judge(dmsg,KeyWords=['help']):
            SendMsg(target,Text='Bot帮助手册:\n\n实时天气: #天气 地区名称\n\n保存图片: 回复相应图片 #pic 名称\n\n发送保存的图片: #mark 图片名称')
            return 0
        #复读
        if Access(target,App='Reply'):
            if 'LastMsg' not in dir(GlobalSet):
                GlobalSet.LastMsg={}
            if len(dmsg['messageChain'])==2 and dmsg['messageChain'][1]['type']=='Image':
                NowMsg=dmsg['messageChain'][1]['imageId']
            else:
                NowMsg=dmsg['messageChain']
                NowMsg.pop(0)
            if str(target) not in GlobalSet.LastMsg:
                GlobalSet.LastMsg[str(target)]=''
            print('\n复读模块消息对比\n',GlobalSet.LastMsg[str(target)],'\n',NowMsg)
            if NowMsg==GlobalSet.LastMsg[str(target)]:
                if type(NowMsg)==list:
                    if randint(1,2)==2:
                        SendMsg(target,msgChain=NowMsg)
                else:
                    SendMsg(target,ImageID=NowMsg)
                GlobalSet.LastMsg[str(target)]=''
            else:
                GlobalSet.LastMsg[str(target)]=deepcopy(NowMsg)
        if Judge(dmsg,ReWords=r'爱[\s\S]*你') and Judge(dmsg,Type='At',target='2090493516'):
            SendMsg(target,Text='么么哒!')
            return 0
        #TimeSend
        

def main():
    Auth()
    CheckSocket()
    asyncio.get_event_loop().run_until_complete(run())

if __name__=='__main__':
    main()
