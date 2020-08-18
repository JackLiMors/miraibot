#-*- coding:utf-8 -*-

from src.ReplyTryRun import TryRun
from src import GlobalSet

@TryRun
def SendMsg(target,Text='',ImageUrl='',ImageID='',AtID='',mode=False,targetType='Group'):

    from requests import post
    from json import loads,dumps
    
    target=int(target)
    URL='http://0.0.0.0:8080'
    if targetType=='Group':
        UrlTail='/sendGroupMessage'
    elif targetType=='Friend':
        UrlTail='/sendFriendMessage'
    elif targetType=='Temp':
        UrlTail='/sendTempMessage'
    elif mode:
        #使用该方法将返回图片ID
        UrlTail='/sendImageMessage'
    else:
        raise Exception('错误的发送对象 targetType:',targetType)

    if mode:
        msg={
                'sessionKey':GlobalSet.sessionKey,
                'group':target,
                'urls':[ImageUrl]
                }
        a=post(URL+UrlTail,dumps(msg))
        return a.text
    else:
        msg={
                'sessionKey':GlobalSet.sessionKey,
                'target':target,
                'messageChain':[]
                }
        if ImageID:
            msg['messageChain'].append({
                'type':'Image',
                'imageId':ImageID
                })
        if ImageUrl:
            msg['messageChain'].append({
                'type':'Image',
                'url':ImageUrl
                })
        if AtID:
            msg['messageChain'].append({
                'type':'At',
                'target':AtID
                })
        if Text:
            msg['messageChain'].append({
                'type':'Plain',
                'text':Text
                })
        if len(msg['messageChain'])<1:
            raise Exception('错误!消息链为空，请检查参数')
        post(URL+UrlTail,dumps(msg))
