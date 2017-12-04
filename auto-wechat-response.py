#发送信息前加'x'触发机器人
#自撩:自己发送消息触发机器人

import requests
import re
import datetime  
import itchat
from itchat.content import *

# turing robot's key
#af65e4c271214da6b79c149bc36085a8 
#c50a6016545749f29e67f151932a6cff
#8edce3ce905a4c1dbb965e6b35c3834d
#d364bd41d25c4c1a9dfcecccf8ed8494
#d5d1200c30f043e5abb14d3fbe9a2659
KEY = 'c50a6016545749f29e67f151932a6cff'

def save_to_log(string):
    f_log = open('log_auto-weather-response.md', 'a')
    f_log.write(string+"\r")
    f_log.close()  
    return

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key' : KEY,
        'info' : msg,
        'userid' : 'wechat-robot',
    }
    try: 
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return 

 
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    if(msg['Text'][0] == '.'):
        defaultReply = msg['Text']#没有响应的时候
        if(msg['FromUserName'] == myID):
            msg['FromUserName'] = msg['ToUserName']#和别人私聊自撩
        reply = '×' + get_response(msg['Text'][1:])#[1:]是除去输入前面的'.'

        now = datetime.datetime.now()  
        save_to_log(now.strftime('%Y/%m/%d %H:%M:%S')+' '+'%10s'%msg['User']['NickName']+' : '+reply or defaultReply)#msg['User']['NickName']用户名
        return reply or defaultReply
    return

# 处理多媒体类消息
# 包括图片、录音、文件、视频
# 处理多媒体类消息
# 包括图片、录音、文件、视频
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    source = msg['FromUserName']
    # msg['Text']是一个文件下载函数
    # 传入文件名，将文件下载下来
    msg['Text'](msg['FileName'])
    # 把下载好的文件再发回给发送者
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 处理好友添加请求
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.add_friend(**msg['Text'])
    # 加完好友后，给好友打个招呼
    itchat.send_msg('.Nice to meet you! --by Turing Robot', msg['RecommendInfo']['UserName'])
 
# 处理群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    #print(msg)#整理出群聊信息
    #if msg['isAt']:#如果被@了
    if(msg['FromUserName'] in white_list.values() or msg['ToUserName'] in white_list.values()) and (msg['Text'][0] == '.'):
        defaultReply = msg['Text']#没有响应的时候
        reply = '×' + get_response(msg['Text'][1:])
        if(msg['ToUserName'] in white_list.values()):#群聊自撩，因为自己在群里发送，则ToUserName是该群聊
            msg['FromUserName'] = msg['ToUserName']

        now = datetime.datetime.now()
        save_to_log(now.strftime('%Y/%m/%d %H:%M:%S')+'  '+'%10s'%msg['User']['NickName']+' : '+reply or defaultReply)#msg['User']['NickName']用户名
        return reply or defaultReply
    return 
 
# 在auto_login()里面提供一个True，即hotReload=True 即可保留登陆状态
itchat.auto_login(hotReload=True,enableCmdQR=2)

now = datetime.datetime.now()  
save_to_log("\r"+"Start in: "+now.strftime('%Y/%m/%d %H:%M:%S'))

myID = itchat.search_friends()['UserName']#获取自己id

white_list = []#白名单
chatroomData = str(itchat.search_chatrooms(name='x'))#填群聊关键词，如有群聊‘呵呵呵’和‘呵哈嘿’，name=‘呵’会抓群id两个
chatroomID = re.findall("(?<='UserName': ')[^']*",chatroomData)#用正则表达式抓取含有关键字的群的id
for i in range(len(chatroomID)):
    if(chatroomID[i][1]=='@'):#因为包含@开头的个人id，所以区分，具体可print chatroomData或msg查看
        white_list.append(chatroomID[i])

itchat.run()
