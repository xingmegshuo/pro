#!/usr/bin/env python
# coding=utf-8
# Author:
# Mail:
# Created Time: 2019年07月31日 星期三 21时24分26秒


import requests
import itchat

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot'
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except BaseException:
        return


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I received:' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or defaultReply


itchat.auto_login(hotReload=True)
itchat.run()
