#-*- coding:utf-8 -*-
#下载模块，保存图片imageID并返回imageID，下载实体文件取消相关注释即可
from src.ReplyTryRun import TryRun
from src import GlobalSet

@TryRun
def Download(name,path,msgID='',msg=''):
    Header={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.116 Chrome/83.0.4103.116 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests':'1'
            }
    from requests import get
    from os import listdir,mkdir
    from json import loads

    msgID=str(msgID)
    if 'Download' not in listdir('src'):
        print('\n初始化下载目录\n*********************\n')
        mkdir('src/Download')
    if path not in listdir('src/Download/'):
        mkdir('src/Download/'+path)
    
    if msgID:
        URL='http://0.0.0.0:8080/messageFromId?sessionKey='+GlobalSet.sessionKey+'&id='+msgID
        msg=loads(get(URL).text)
        if msg['code']==5:
            return '未找到指定聊天记录\n可能是因为期间机器人进行了重启，或者消息丢失导致的'
        Url=msg['data']['messageChain'][1]['url']
        ImageID=msg['data']['messageChain'][1]['imageId']
        if 'ImageIDList' not in dir(GlobalSet):
            GlobalSet.ImageIDList={}
        GlobalSet.ImageIDList[name]=ImageID
        if path not in listdir('/var/www/html/Download/'):
            mkdir('/var/www/html/Download/'+path)
        #with open('/var/www/html/Download/'+path+'/'+name,'wb') as f:
        #    f.write(get(Url,headers=Header).content)
        return '下载成功'
    else:
        for i in msg['messageChain']:
            if 'url' in i:
                url=i['url']
                imageid=i['imageId']
                break
        try:
            #with open('/var/www/html/Download/'+path+'/'+name,'wb') as f:
            #    f.write(get(url,headers=Header).content)
            GlobalSet.ImageIDList[name]=imageid
            return '下载成功'
        except Exception:
            return '下载失败'
