#-*- coding:utf-8 -*-
#图片模块，包括随机发送和指定发送、保存图片，这个模块写的有些混乱：
#原本通过nginx和本地url发送，后来改为imageID发送之后，文件的路径改混乱了
from src.ReplyTryRun import TryRun
from src.ReplyDownload import Download
from src.ReplySendMsg import SendMsg
from src import GlobalSet

@TryRun
def Pic(target,path,name='',msgID='',msg=''):
    #此函数兼顾发送保存的指定图片，发送保存的随机图片
    from os import listdir,mkdir
    from json import loads,dumps
    from random import randint

    MainPath='/var/www/html/Download'
    if 'PicIDList' not in dir(GlobalSet):
        GlobalSet.PicIDList={}
    GlobalSet.DownloadPathList=listdir('/var/www/html/Download')
    #保存图片
    if msgID:
        if name:
            SendMsg(target,Text=Download(name,path,msgID=msgID))
        else:
            SendMsg(target,Text=Download(str(msgID),path,msgID=msgID))
            name=str(msgID)
        if name in GlobalSet.ImageIDList:
            if path not in GlobalSet.PicIDList:
                if path in GlobalSet.DownloadPathList:
                    if path+'IDList' in listdir(MainPath+'/'+path):
                        with open(MainPath+'/'+path+'/'+path+'IDList') as f:
                            GlobalSet.PicIDList[path]=loads(f.read())
                    else:
                        GlobalSet.PicIDList[path]={'name':[],'num':0,'id':[]}
                else:
                    GlobalSet.PicIDList[path]={'name':[],'num':0,'id':[]}
            GlobalSet.PicIDList[path]['name'].append(name)
            GlobalSet.PicIDList[path]['num']+=1
            GlobalSet.PicIDList[path][name]=GlobalSet.ImageIDList[name]
            if 'id' not in GlobalSet.PicIDList[path]:
                GlobalSet.PicIDList[path]['id']=[]
            GlobalSet.PicIDList[path]['id'].append(GlobalSet.ImageIDList[name])
        with open('/var/www/html/Download/'+path+'/'+path+'IDList','w') as f:
            f.write(dumps(GlobalSet.PicIDList[path]))
        return 0
    if msg:
        SendMsg(target,Text=Download(name,path,msg=msg))
        if name in GlobalSet.ImageIDList:
            if path not in GlobalSet.PicIDList:
                if path in GlobalSet.DownloadPathList:
                    if path+'IDList' in listdir(MainPath+'/'+path):
                        with open(MainPath+'/'+path+'/'+path+'IDList') as f:
                            GlobalSet.PicIDList[path]=loads(f.read())
                    else:
                        GlobalSet.PicIDList[path]={'name':[],'num':0,'id':[]}
                else:
                    GlobalSet.PicIDList[path]={'name':[],'num':0,'id':[]}
            GlobalSet.PicIDList[path]['name'].append(name)
            GlobalSet.PicIDList[path]['num']+=1
            GlobalSet.PICIDList[path][name]=GlobalSet.ImageIDList[name]
            GlobalSet.PicIDList[path]['id'].append(GlobalSet.ImageIDList[name])
        with open('/var/www/html/Download/'+path+'/'+path+'IDList','w') as f:
            f.write(dumps(GlobalSet.PicIDList[path]))
        return 0
    #发送图片    
    if path not in GlobalSet.PicIDList:
        if 'Download' not in listdir('src'):
            print('\n初始化下载目录\n*********************\n')
            mkdir('/var/www/html/Download/')
            mkdir('/var/www/html/Download/'+path)
            GlobalSet.PicIDList[path]={'name':[],'num':0}
            SendMsg(target,Text='你还没有保存图片')
            return 0
        elif path not in listdir('/var/www/html/Download/'):
            mkdir('/var/www/html/Download/'+path)
            GlobalSet.PicIDList[path]={'name':[],'num':0}
            SendMsg(target,Text='你还没有保存图片')
            return 0
        elif path+'IDList' not in listdir('/var/www/html/Download/'+path):
            GlobalSet.PicIDList[path]={'name':[],'num':0}
        else:
            with open('/var/www/html/Download/'+path+'/'+path+'IDList','r') as f:
                GlobalSet.PicIDList[path]=loads(f.read())
            #GlobalSet.PicIDList[path]['name']=listdir('/var/www/html/Download/'+path+'/')
            #GlobalSet.PicIDList[path]['name'].remove(path+'IDList')
            #GlobalSet.PicIDList[path]['num']=len(GlobalSet.PicIDList[path]['name'])
    
    if GlobalSet.PicIDList[path]['num']==0:
        GlobalSet.PicIDList[path]['name']=listdir('/var/www/html/Download/'+path)
        if path+'IDList' in GlobalSet.PicIDList[path]['name']:
            GlobalSet.PicIDList[path]['name'].remove(path+'IDList')
        GlobalSet.PicIDList[path]['num']=len(GlobalSet.PicIDList[path]['name'])
    if GlobalSet.PicIDList[path]['num']<1:
        SendMsg(target,Text='你还没有保存图片')   
        return 0

    if name:
        if name in GlobalSet.PicIDList[path]['name']:
            if name in GlobalSet.PicIDList[path]:
                print('\n发送图片:',GlobalSet.PicIDList[path][name],'\n')
                SendMsg(target,ImageID=GlobalSet.PicIDList[path][name])
                return 0
            #else:
                #print('\n发送图片:',name,'\n')
                #a=SendMsg(target,ImageUrl='http://127.0.0.1:30000/'+path+'/'+name,mode=True)
                #return 0
                ######
        else:
            SendMsg(target,Text='你还没有保存图片: '+name)
            return 0
    else:
        name=GlobalSet.PicIDList[path]['id'][randint(0,GlobalSet.PicIDList[path]['num']-1)]
        #if name not in GlobalSet.PicIDList[path]:
            #print('\n发送图片:','http://127.0.0.1:30000/'+path+'/'+name,'\n')
            #a=SendMsg(target,ImageUrl='http://127.0.0.1:30000/'+path+'/'+name)
            #print(a)
            #SendMsg(target,Text='图库中没有任何图片')
        #else:
        print('\n发送图片:',name,'\n')
        SendMsg(target,ImageID=name)
