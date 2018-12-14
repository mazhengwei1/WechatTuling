# -*- coding: utf-8 -*-

# @Time    : 2018/12/14
# @Author  : Macus
# @Email   : 13720433512@163.com    
# @Site    : http://www.wei1011.club
# @File    : index.py
# @Software: PyCharm          实现微信机器人自动回复

import itchat
import requests
import json
from itchat.content import *

# 图灵调用函数
def get_response(info):
    '''
    用爬虫方式传入好友消息,并获取返回图灵机器人的回复

    '''
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    dat = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": info
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "西安",
                    "province": "陕西",
                    "street": "周至县"
                }
            }
        },
        "userInfo":{
            'apiKey': '3a54a334f1a24da384969c4d94842ac4',
            'userId': 'sunmingbo',
        },
    }
    r = ''
    try:
        dat = json.dumps(dat)
        response = requests.post(url, data=dat).json()
        print(response)
        try:
            r = response['results'][0]['values']['text']
        except TypeError as f:
            # print(f)
            r = str(response['results'][0]['values']['url'])
            r += '\n'
            r += response['results'][1]['values']['text']
        except Exception as w:
            r = "你说什么,我听不懂"

    except Exception as e:
        r = "你说什么,我听不懂"
    # print(response)
    print(r)
    return r
def main():
    '''
    处理各种消息
    '''
    def group_id():
        # 对于群聊消息,定义获取想要针对某个群进行机器人回复的群ID函数
        groups = itchat.get_chatrooms(update=True)
        # print(groups)
        group_names = []
        for i in range(len(groups)):
            group_name = groups[i]['NickName']
            # if '中三1婚姻介绍所-8群' in group_name:
            group_names.append(group_name)
            return group_names

    # 注册文本消息,好友消息处理函数
    @itchat.msg_register(TEXT, isFriendChat=True)
    def fri_reply(msg):
        # msg为要回复给对象的消息, toUserName为要回复的对象
        itchat.send(msg=get_response(msg['Text']), toUserName=msg['FromUserName'])

    @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def file_download(msg):
        # 文件下载函数
        msg['Text'](msg['FileName'])
        return '@%s@%s' % ({'Picture': 'img', 'Video': 'video'}.get(msg['Type'], 'fil'), msg['FileName'])

    # 群消息回复
    @itchat.msg_register(TEXT, isGroupChat=True)
    def group_reply(msg):
        group_names = group_id()   #获取所有群聊名称
        if msg['FromUserName'] != '@@812fc4f7c0460317d4053847926a10fd45fba7645e3b4762124133d6c13c906c':
            # 如果不是特定群名不回复.
            print("不回复", msg['FromUserName'], msg['ActualNickName'])   # 群名和at你的人网名
            return
        # 只有在at你的情况下才回复
        if msg['isAt']:
            content = msg['Text']
            info = content
            # print(content)   content内容为:@自己微信名字 不想你
            if '走马观花' in content:    # 改成你自己的微信名字
                info = str(content).replace('走马观花', '')
            itchat.send(msg=u'%s' % get_response(info), toUserName=msg['FromUserName'])

if __name__ == "__main__":
    itchat.auto_login(hotReload=True)
    main()
    itchat.run()



