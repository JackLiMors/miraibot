# 使用Python编写的mriaiOK QQbot消息处理脚本，基于http-api插件  

## 使用方法  
**只适用于Linux amd64架构**  
注意你需要安装tmux或者screen(这里使用tmux)，而且只在Ubuntu上作了测试，以下以tmux为例，在使用之前可能你需要熟悉以下tmux的指令  
```
sudo apt install tmux
git clone https://gitee.com/syize_admin/miraibot.git
cd miraibot
tmux
```

下面的代码都在tmux中执行
```
ctrl+B % #分出两个屏幕
./miraiOK_linux_amd64 #运行miraiOK一键配置脚本，记下http-apt插件给出的authKey
login QQ号 密码 #登陆QQ
ctrl+B ↓ #切换到另一个分屏
./BotReply #运行脚本
ctrl+B D #分离终端
```

## 已经写出的功能
程序编写完全模块化，你可以自己根据需求添加相应的功能  
> 1.判断消息和发送消息(包括文本消息、图片消息(分为url发送和imageID发送两种)、At消息、混合消息  
> 2.下载图片功能(保存图片imageID，如果你想下载图片文件可以取消相应注释)  
> 3.从公共的图库中随机发送图片 ~~涩图功能~~  
> 4.从个人的图库中随机发送图片  
> 5.发送个人保存的指定图片  
> 6.复读功能  
> 7.简短的实时天气功能(使用了和风天气API)  
> 8.权限功能  
> 9.禁言功能(最高时长3分钟)，解除禁言功能  
> 10.招新功能
> 11.错误处理功能(使用装饰器实现，当出现错误是会通过私聊形式将错误日志发送给超级管理员)  

## 待实现的功能  
> 暂时没想出来  


