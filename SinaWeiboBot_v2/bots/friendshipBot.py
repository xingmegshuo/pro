#coding=utf-8
import re
import logging
import sinaRequests as requests
import config
from . import CreateBaseBot
from utils import tag


friendshipUrl = 'https://m.weibo.cn/api/friendships/create'

class FriendshipBot(CreateBaseBot):

    name = 'friendship'
    
    def __init__(self, taskid, params):
        cookies = params['cookies']
        uid = str(params['uid'])
        self.st = params['st']
        super(FriendshipBot, self).__init__(taskid, uid, cookies)
        self.targetuid = str(params['targetuid'])

    def createReq(self):
        self.checkUserExist()
        data = {
            'uid': self.targetuid,
            'st': self.st,
        }
        resp = self.session.post(friendshipUrl, headers=config.HEADER, data=data)
        logging.debug(tag('friendship create response: %s' % resp.text))
        return resp

    def checkUserExist(self):
        url = 'https://m.weibo.cn/profile/info?uid=' + self.targetuid
        resp = requests.get(url, headers=config.HEADER)
        if re.findall(r'用户不存在', resp.text):
            self.err = 1
            self.reason = config.REASON['account_not_found']

    def successData(self):
        return {
            'targetuid': self.targetuid,
        }