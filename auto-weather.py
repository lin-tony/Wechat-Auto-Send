import re
import datetime  
import requests      
import os
import itchat
import time  
from itchat.content import *

# turing robot's key
#af65e4c271214da6b79c149bc36085a8 
#c50a6016545749f29e67f151932a6cff
#8edce3ce905a4c1dbb965e6b35c3834d
#d364bd41d25c4c1a9dfcecccf8ed8494
#d5d1200c30f043e5abb14d3fbe9a2659
KEY = '8edce3ce905a4c1dbb965e6b35c3834d' 
    
def save_to_log(string):
    f_log = open('log_auto-weather.md', 'a')
    f_log.write(string+"\r")
    f_log.close()  
    return

def get_response(msg):    
    apiUrl = 'http://www.tuling123.com/openapi/api'    
    data = {    
        'key'    : KEY,    
        'info'   : msg,    
        'userid' : 'wechat-robot',    
    }    
    try:    
        r = requests.post(apiUrl, data=data).json()    
        return r.get('text')    
    except:    
        return    
    
#回复内容
def tuling_reply(addr,username):
    weather_reply = get_response(addr+'明天天气')
    save_to_log(weather_reply)
    itchat.send(weather_reply,toUserName=username)

def tuling_reply_to_personal(addr,username):
    weather_reply = """for xxx:"""+get_response(addr+'明天天气')
    save_to_log(weather_reply)
    itchat.send(weather_reply,toUserName=username)

# 在auto_login()里面提供一个True，即hotReload=True 即可保留登陆状态，enableCmdQR=TRUE/2命令行二维码
itchat.auto_login(hotReload=True) 

#以下是发送到群聊

addr_list = ['x','x'] #输入发送天气地点  
white_list = []#白名单
chatroomData = str(itchat.search_chatrooms(name='x'))#填群聊关键词，如有群聊‘呵呵呵’和‘呵哈嘿’，name=‘呵’会抓群到两个
chatroomID = re.findall("(?<='UserName': ')[^']*",chatroomData)#用正则表达式抓取含有关键字的群的id
for i in range(len(chatroomID)):
    if(chatroomID[i][1]=='@'):#因为包含@开头的个人id，所以区分，具体可print chatroomData查看
        white_list.append(chatroomID[i])

#以下是给个人到群聊
personaluser=itchat.search_friends(name='xxx')  #输入ta的备注  
personalusername=personaluser[0]['UserName']  
personaladdr='x'

now = datetime.datetime.now()  
now_str = now.strftime('%Y/%m/%d %H:%M:%S')
save_to_log("\r"+'Start in: '+now_str)

while 1:  
    now = datetime.datetime.now()  
    now_str = now.strftime('%Y/%m/%d %H:%M')[11:]
    save_to_log(now_str)

    if now_str in ['23:30']:  # 发送时间
        tuling_reply_to_personal(personaladdr,personalusername)
        for i in white_list:
            for addr in addr_list:
                tuling_reply(addr,i)
        time.sleep(72600)
    time.sleep(50)
