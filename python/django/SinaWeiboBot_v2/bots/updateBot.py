#coding=utf-8
import logging
import sinaRequests as requests
import config
from . import CreateBaseBot
from utils import tag

updateUrl = 'https://m.weibo.cn/api/statuses/update'

class UpdateBot(CreateBaseBot):

    name = 'update'
    
    def __init__(self, taskid, params):
        cookies = params['cookies']
        uid = str(params['uid'])
        self.st = params['st']
        super(UpdateBot, self).__init__(taskid, uid, cookies)

        self.content = params['content']

    def createReq(self):
        data = {
            'content': self.content,
            'st': self.st,
        }
        resp = self.session.post(updateUrl, headers=config.HEADER, data=data)
        logging.debug(tag('update response: %s' % resp.text))
        self.checkRepeat(resp)
        return resp

    def successData(self):
        return {
            'content': self.content,
        }