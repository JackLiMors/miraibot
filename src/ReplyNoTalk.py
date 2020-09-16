#-*- coding:utf-8 -*-
#禁言模块，上限三分钟，可更改
from src.ReplyTryRun import TryRun
from src import GlobalSet

@TryRun
def NoTalk(msg,level=1,mode='set'):
    from requests import post
    from json import loads,dumps

    for i in msg['messageChain']:
        if i['type']=='At':
            member=i['target']
            break

    target=msg['sender']['group']['id']
    Level={
            1:60,
            2:120,
            3:180
            }
    
    msg={
            'sessionKey':GlobalSet.sessionKey,
            'target':target,
            'memberId':member
            }
    if mode=='set':
        msg['time']=Level[level]
        a=post('http://0.0.0.0:8080/mute',dumps(msg))
        A=loads(a.text)
        if A['code']!=0:
            return '上茶失败'
        else:
            return '给👴爪巴'
    elif mode=='unset':
        a=post('http://0.0.0.0:8080/unmute',dumps(msg))
        A=loads(a.text)
        if A['code']!=0:
            return '差太多啦下不完啦'
        else:
            return '欢迎再来!'
