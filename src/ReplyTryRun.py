#!/usr/bin/python3
#该函数是一个装饰器，每个新模块建议都引入并加装，防止意料之外的错误导致进程停止
from traceback import format_exc
from src import GlobalSet

def TryRun(func):
    def ReplyError(*args,**kw):
        try:
            text=func(*args,**kw)
            return text
        except Exception:
            errorlog=format_exc()
            errorlog='有错误发生!\n运行日志:\n'+errorlog
            print('\nWARNNING:\n',errorlog)
            from requests import post
            from json import dumps
            msg={
                    'sessionKey':GlobalSet.sessionKey,
                    'target':GlobalSet.AdminQQ,
                    'messageChain':[{
                        'type':'Plain',
                        'text':errorlog
                        }]
                    }
            post('http://0.0.0.0:8080/sendFriendMessage',dumps(msg))
            return errorlog
    return ReplyError
