#coding=utf-8
import logging, time, random, re, copy
from datetime import datetime, timedelta
import http.cookiejar as cookielib
import sinaRequests as requests
import config
from . import BaseBot
from utils import tag
#这个应该是抓取好友更新动态
friendsUrl = 'https://m.weibo.cn/feed/friends'

class CrawlFriends(BaseBot):

    name = 'crawl_friends'

    def __init__(self, taskid, params):
        super(CrawlFriends, self).__init__(taskid)
        cookies = params['cookies']
        uid = str(params['uid'])
        st = params['st']
        ua = params['ua']
        self.headers = copy.deepcopy(config.HEADER)
        self.headers['User-Agent'] = ua
        self.pageno = int(params['pageno'])
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
        blogs = []
        max_id = None
        for _ in range(self.pageno):
            if max_id:
                url = friendsUrl + '?max_id=' + str(max_id)
            else:
                url = friendsUrl
            resp = self.session.get(url, headers=self.headers)
            if re.findall('暂无数据', resp.text):
                break
            for blog in resp.json()['data']['statuses']:
                uid = blog['user']['id']
                blog_mid = blog['mid']
                created_at = blog['created_at']
                created_at = time.strptime(created_at.replace('+0800 ', ''), "%a %b %d %H:%M:%S %Y")
                created_at = time.strftime("%Y-%m-%d %H:%M:%S", created_at)
                summary = blog['text'][:20]
                blogs.append({
                    'uid': uid,
                    'blog_mid': blog_mid,
                    'created_at': created_at,
                    'summary': summary,
                })
            max_id = resp.json()['data']['max_id']
        self.data['blogs'] = blogs

                


