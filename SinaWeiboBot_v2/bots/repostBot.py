#coding=utf-8
import logging, time, random
import sinaRequests as requests
import config
from . import CreateBaseBot
from utils import tag

repostUrl = 'https://m.weibo.cn/api/statuses/repost'

class RepostBot(CreateBaseBot):

    name = 'repost'

    def __init__(self, taskid, params):
        cookies = params['cookies']
        uid = str(params['uid'])
        st = params['st']
        super(RepostBot, self).__init__(taskid, uid, cookies, st)
        self.targetid = str(params['targetid'])
        self.targetmid = str(params['targetmid'])
        self.checkBlogExist_id = self.targetid
        self.content = '转发微博'
        if 'content' in params:
            if params['content']:
                if params['content'] != 'None':
                    self.content = str(params['content'])
        if 'content' in params and params['content']:
            self.content = str(params['content'])
        self.dualPost = 1 if int(params['dualPost']) else 0

    def createReq(self):
        # self.readIndex()
        self.checkBlogExist()
        if self.err:
            return
        time.sleep(config.OPERATE_REPOST_DELAY())
        data = {
            'id': self.targetid,
            'content': self.content,
            'dualPost': self.dualPost,
            'mid': self.targetmid,
            'st': self.st,
        }
        resp = self.session.post(repostUrl, headers=self.headers, data=data)
        logging.debug(tag('repost response: %s' % resp.text))
        self.checkRepeat(resp)
        if resp.json().get('msg') == '发微博太多啦，休息一会儿吧!':
            self.reason = config.REASON['frequent_repost']
            self.err = 1
        return resp

    def successData(self):
        return {
            'targetid': self.targetid,
            'targetmid': self.targetmid,
            'content': self.content,
            'dualPost': self.dualPost,
        }

class FastRepostBot(RepostBot):

    name = 'fast_repost'

# {
#   "ok": 0,
#   "errno": "20019",
#   "msg": "相同内容请间隔10分钟再进行发布哦！",
#   "error_type": "alert"
# }