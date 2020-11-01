#coding=utf-8
import json, time, logging
import sinaRequests as requests
import config
from . import CreateBaseBot
from utils import tag



heartUrl = 'https://m.weibo.cn/api/attitudes/create'

class HeartBot(CreateBaseBot):

    name = 'heart'

    def __init__(self, taskid, params):
        cookies = params['cookies']
        uid = str(params['uid'])
        st = params['st']
        super(HeartBot, self).__init__(taskid, uid, cookies, st)
        self.targetid = str(params['targetid'])
        self.checkBlogExist_id = self.targetid

    def createReq(self):
        # self.readIndex()
        self.checkBlogExist()
        if self.err:
            return
        time.sleep(config.OPERATE_HEART_DELAY())
        data = {
            'id': self.targetid,
            'attitude': 'heart',
            'st': self.st,
        }
        logging.info(tag('heart create req data: %s' % json.dumps(data)))
        resp = self.session.post(heartUrl, headers=self.headers, data=data)
        logging.info(tag('heart create response: %s' % resp.text))
        if resp.json().get('msg') == '操作失败':
            self.reason = config.REASON['heart_operate_fail']
            self.err = 1
        return resp

    def successData(self):
        return {
            'targetid': self.targetid,
        }

class FastHeartBot(HeartBot):

    name = 'fast_heart'