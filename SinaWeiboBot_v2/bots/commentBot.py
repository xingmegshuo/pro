#coding=utf-8
import logging, time, random, json
import sinaRequests as requests
import config
from . import CreateBaseBot, comments
from utils import tag

commentUrl = 'https://m.weibo.cn/api/comments/create'
#评论接口
class CommentBot(CreateBaseBot):

    name = 'comment'

    def __init__(self, taskid, params):
        cookies = params['cookies']
        uid = str(params['uid'])
        st = str(params['uid'])
        super(CommentBot, self).__init__(taskid, uid, cookies, st)

        self.targetmid = str(params['targetmid'])
        self.content = str(params['content'])
        self.checkBlogExist_id = self.targetmid

    def createReq(self):
        # self.readIndex()
        self.checkBlogExist()
        if self.err:
            return
        time.sleep(config.OPERATE_COMMENT_DELAY(len(self.content)))
        data = {
            'content': self.content,
            'mid': self.targetmid,
            'st': self.st,
        }
        logging.info(tag('comment req data: %s' % json.dumps(data)))
        resp = self.session.post(commentUrl, headers=self.headers, data=data)
        logging.info(tag('comment response: %s' % resp.text))
        self.checkRepeat(resp)
        if resp.json().get('msg') == '发微博太多啦，休息一会儿吧!':
            self.reason = config.REASON['frequent_comment']
            self.err = 1
        if resp.json().get('msg') == '作者只允许粉丝评论!':
            self.reason = config.REASON['only_allows_fans_comment']
            self.err = 1
        return resp

    def successData(self):
        return {
            'content': self.content,
            'targetmid': self.targetmid,
        }

class FastCommentBot(CommentBot):

    name = 'fast_comment'
