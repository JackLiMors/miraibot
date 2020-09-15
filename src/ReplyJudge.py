#-*- coding:utf-8 -*-

from src.ReplyTryRun import TryRun
from src import GlobalSet

@TryRun
def Judge(msg,KeyWords='',ReWords='',Type='Plain',target='',mode='strict'):
    from re import compile
    part={};step=0
    for i in msg['messageChain']:
        if i['type'] in part:
            part[i['type']].append(step)
        else:
            part[i['type']]=[step,]
        step+=1


    if Type=='Plain':
        if KeyWords:
            if type(KeyWords)!=list and type(KeyWords)!=tuple:
                raise Exception('KeyWords应为一个列表或tuple')
            flag=True
            if 'Plain' not in part:
                return False
            for i in part['Plain']:
                textlist=msg['messageChain'][i]['text'].split()
                if len(textlist)<len(KeyWords):
                    return False
                for a,b in zip(KeyWords,textlist):
                    if a!=b:
                        flag=False
                if flag:
                    return True
                else:
                    flag=True
            return False
        elif ReWords:
            Re=compile(ReWords)
            if 'Plain' not in part:
                return False
            flag=False
            for i in part['Plain']:
                if Re.search(msg['messageChain'][i]['text']):
                    flag=True
            return flag
        else:
            raise Exception('缺少必要的判断参数')
    if Type=='At':
        if 'At' not in part:
            return False
        if target:
            for i in part['At']:
                if target==str(msg['messageChain'][i]['target']):
                    return True
            return False
        else:
            return True
    if Type=='Image':
        if 'Image' in part:
            return True
        else:
            return False
    if Type=='Quote':
        if 'Quote' in part:
            return True
        else:
            return False
    raise Exception('未指定判断的类型')
