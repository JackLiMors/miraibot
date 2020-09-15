#!/usr/bin/python3

from src.ReplyTryRun import TryRun
from src import GlobalSet

@TryRun
def Count(msg):
    if 'Count' not in dir(GlobalSet):
        GlobalSet.Count=[]
    groupID=msg['sender']['group']['id']
    ID=msg['sender']['id']
    if groupID==564307340 and ID not in GlobalSet.Count:
        GlobalSet.Count.append(ID)
        with open('src/Cache/Count','w') as f:
            for i in GlobalSet.Count:
                f.write(str(i)+' ')
    return 0
