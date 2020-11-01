#coding=utf-8
import logging, time, random, re, copy
from datetime import datetime, timedelta
import http.cookiejar as cookielib
import sinaRequests as requests
import config
from . import BaseBot
from utils import tag

friendsUrl = 'https://m.weibo.cn/feed/friends'
#读取消息列表中是否包含帐号异常信息
class CrawlSecurityBot(BaseBot):

    name = 'crawl_security'

    def __init__(self, taskid, params):
        super(CrawlSecurityBot, self).__init__(taskid)
        cookies = params['cookies']
        uid = str(params['uid'])
        st = params['st']
        ua = params['ua']
        self.headers = copy.deepcopy(config.HEADER)
        self.headers['User-Agent'] = ua
        self.session = self.initSession(uid, cookies)

    def initSession(self, uid, cookies):
        session = requests.session()
        cookiefile = config.CACHE_DIR + '/' + uid + '.cookies'
        with open(cookiefile, 'w') as f:
            f.write(cookies)
        self.cachefiles.append(cookiefile)
        session.cookies = cookielib.LWPCookieJar()
        session.cookies.load(filename=cookiefile)
        logging.info(tag('init session uid: %s' % uid))
        return session

    def crawl(self):
        msgs = []
        url = 'https://m.weibo.cn/message/msglist?page=1'
        self.url = 'https://m.weibo.cn/message/msglist'
        resp = self.session.get(url)
        self.response = resp.json()
        security_uid = None
        for i in resp.json()['data']:
            if i['user']['screen_name'] == '微博安全中心':
                security_uid = i['user']['id']
        if security_uid:
            msgurl = 'https://m.weibo.cn/api/chat/list'
            self.url = msgurl
            params = {
                'uid': security_uid,
                'count': 10,
                'unfollowing': 0,
            }
            resp = self.session.get(msgurl, params=params)
            self.response = resp.json()
            verify_url = None
            for i in resp.json()['data']['msgs']:
                # 提取账户异常，解除异常的链接
                text = i['text']
                id = i['id']
                created_at = i['created_at']
                created_at = time.strptime(created_at.replace('+0800 ', ''), "%a %b %d %H:%M:%S %Y")
                created_at = time.strftime("%Y-%m-%d %H:%M:%S", created_at)
                msgs.append({
                    'text': text,
                    'id': id,
                    'created_at': created_at,
                })
        else:
            logging.info(tag('no security msg'))
        self.data['msgs'] = msgs

                


