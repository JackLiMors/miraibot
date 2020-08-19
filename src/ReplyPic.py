#-*- coding:utf-8 -*-

from src.ReplyTryRun import TryRun
from src.ReplyDownload import Download
from src.ReplySendMsg import SendMsg

@TryRun
def Pic(target,path,name='',msgID=''):
    #此函数兼顾发送保存的指定图片，发送保存的随机图片
    from os import listdir
    from json import loads,dumps
    from random import randint

    if 'PicIDList' not in dir(GlobalSet):
        GlobalSet.PicIDList={}

    else:
        if path not in GlobalSet.PicIDList:
            if 'Download' not in listdir('src'):
                print('\n初始化下载目录\n*********************\n')
                mkdir('src/Download')
                mkdir('src/Download/'+path)
                GlobalSet.PicIDList[path]={}
                SendMsg(target,Text='你还没有保存图片')
            elif path not in listdir('src/Download'):
                mkdir('src/Download/'+path)
                GlobalSet.PicIDList[path]={}
                SendMsg(target,Text='你还没有保存图片')
            elif path+'IDList' not in listdir('src/Download/'+path):
                GlobalSet.PicIDList[path]={}
                SendMsg(target,Text='你还没有保存图片')
            else:
                with open('src/Download/'+path+'/'+path+'IDList','r') as f:
                    GlobalSet.PicIDList[path]=loads(f.read())
        
        if 'name' not in GlobalSet.PicIDList[path]:
            GlobalSet.PicIDList[path]['name']=listdir('src/Download/'+path)
            if path+'IDList' in GlobalSet.PicIDList[path]['name']:
                GlobalSet.PicIDList[path]['name'].remove(path+'IDList')
            GlobalSet.PicIDList[path]['num']=len(GlobalSet.PicIDList[path]['name'])

        if GlobalSet.PicIDList[path]['num']<1:
            SendMsg(target,Text='你还没有保存图片')

        name=GlobalSet.PicIDList[path]['name'][randint(0,GlobalSet.PicIDList[path]['num'])]
        if name not in GlobalSet.PicIDList[path]:
            a=SendMsg(target,ImageUrl='http://127.0.0.1:8000/'+path+'/'+name,mode=True)
            print(a)
        else:
            SendMsg(target,ImageID=GlobalSet.PicIDList[path][name])
