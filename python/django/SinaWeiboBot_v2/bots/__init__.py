# coding=utf-8
import os, copy, re, logging, traceback
import http.cookiejar as cookielib
from requests.exceptions import ConnectionError as requests_ConnectionError
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout 
import sinaRequests as requests
import config
from utils import tag, timestamp


configUrl = 'https://m.weibo.cn/api/config'

class BaseBot(object):

    def __init__(self, taskid):
        self.taskid = taskid
        self.data = {}
        self.traceback = None
        self.cachefiles = []


        self.code = 0
        self.subcode = None
        self.url = None
        self.response = None

        # code：0，成功，
        # 1，网络错误，
        # 2，打码服务错误
        # 3、登陆错误
        # 4、帐号异常
        # 5、操作异常
        # 6、未知异常

    def __repr__(self):
        return '%s<%s:%s>' % (self.__class__.__name__, self.name, self.taskid)

    def run(self):
        start_at = timestamp()
        try:
            self.crawl()
        except Exception as e:
            logging.info(tag(str(e)))
            if e is KeyboardInterrupt:
                self.clearcache()
                raise KeyboardInterrupt
            if isinstance(e, requests_ConnectionError) or isinstance(e, ConnectTimeout) or isinstance(e, ReadTimeout):
                self.code = 1
                self.subcode = 1001
                # self.err = 1
                # self.reason = config.REASON['net_err']
                # self.traceback = traceback.format_exc()
            else:
                self.code = 6
                # self.err = 1
                # self.reason = config.REASON['bot_run_error']
                self.traceback = traceback.format_exc()
        finished_at = timestamp()
        self.data['start_at'] = start_at
        self.data['finished_at'] = finished_at
        self.clearcache()

    def crawl(self):
        pass

    def clearcache(self):
        for i in self.cachefiles:
            if os.path.exists(i):
                os.remove(i)

    def isNetError(self, status_code):
        supervisorInfo = {}
        if status_code == 418 or status_code == 414:
            self.err = 1
            self.reason = config.REASON['ip_forbidden']
        if status_code == 599:
            self.err = 1
            self.reason =  config.REASON['bad_vpn']



class CreateBaseBot(BaseBot):
    
    def __init__(self, taskid, uid, cookies, st=None):
        self.uid = uid
        self.cookies = cookies
        self.st = st
        super(CreateBaseBot, self).__init__(taskid)
        self.checkBlogExist_id = None
        self.headers = append_xsrf_header(self.st)

    def initSession(self):
        session = requests.session()
        cookiefile = config.CACHE_DIR + '/' + self.uid + '.cookies'
        # print(cookiefile)
        # print(self.cookies)
        with open(cookiefile, 'w') as f:
            f.write(self.cookies)
        self.cachefiles.append(cookiefile)
        session.cookies = cookielib.LWPCookieJar()
        session.cookies.load(filename=cookiefile)
        logging.info(tag('init session uid: %s' % self.uid))
        return session

    def isExpired(self, session):
        resp = session.get(configUrl, headers=self.headers)
        logging.info(tag('config response: %s' % resp.text))
        data = resp.json()
        msg = data.get('msg')
        if msg:
            if msg == '请求过于频繁,歇歇吧':
                self.err = 1
                if self.name == 'fast_heart':
                    self.reason = config.REASON['heart_operate_fail']
                if self.name == 'fast_repost':
                    self.reason = config.REASON['frequent_repost']
                if self.name == 'fast_comment':
                    self.reason = config.REASON['frequent_comment'] 
                return
        data = resp.json()['data']
        if data['login']:
            st = data['st']
            return st
        self.reason =  config.REASON['account_expired']
        self.err = 1

    def checkBlogExist(self):
        url = 'https://m.weibo.cn/detail/' + self.checkBlogExist_id
        resp = self.session.get(url, headers=self.headers)
        if re.findall(r'微博不存在或暂无查看权限!', resp.text):
            logging.error(tag(resp.url))
            logging.error(tag(resp.text))
            self.reason =  config.REASON['blog_not_found']
            self.err = 1

    def readIndex(self):
        url = 'https://m.weibo.cn/'
        resp = self.session.get(url, headers=self.headers)
        url = 'https://m.weibo.cn/api/config'
        resp = self.session.get(url, headers=self.headers)
        print(resp.text)

    def crawl(self):
        self.session = self.initSession()
        # self.isExpired(self.session)
        self.st = self.isExpired(self.session)
        self.headers = append_xsrf_header(self.st)
        if self.err:
            return
        resp = self.createReq()
        if self.err:
            return
        self.checkAccountForbidden(resp)
        if self.err:
            return
        if resp.json()['ok'] == 1:
            self.reason = config.REASON['done']
            self.data = self.successData()
            return
        # {
        #     "ok": 0,
        #     "errno": "100006",
        #     "msg": "token校验失败"
        # }
        # {
        #     "ok": 0,
        #     "errno": "20021",
        #     "msg": "抱歉，根据相关法律法规的要求，此内容无法发布。",
        #     "error_type": "alert"
        # }
        if resp.json().get('msg') == 'token校验失败':
            self.err = 1
            self.reason = config.REASON['account_expired']
            return
        if resp.json().get('msg') == '由于作者隐私设置，你没有权限评论此微博':
            self.reason = config.REASON['no_permission']
            self.err = 1
            return
        if resp.json().get('msg') == '抱歉，根据相关法律法规的要求，此内容无法发布。':
            self.reason = config.REASON['censor_forbidden']
            self.err = 1
            return
        logging.error(tag(resp.text))
        self.reason = config.REASON['bot_run_error']
        self.err = 1

    def checkAccountForbidden(self, resp):
        # 点赞任务：账户被封、目标博文不存在 msg 都为'操作失败'
        # 关注任务：账户被封、目标用户不存在 msg 都为'用户不存在'
        # 对于这个两个任务，执行之前会提前访问博文页或用户页检测是否存在，
        # 执行任务之后，运行到此函数是，再返回 '操作失败'、'用户不存在'，则判定为账户被封

        # 修改：去除对点赞返回 操作失败的检查，对于这种情况不在判断为账户异常，
        # 而是返回新的错误类型，避免账户状态的误判，因为短时间内点赞超过 15 次，也会返回操作失败
        msg = resp.json().get('msg')
        # if msg == '帐号处于锁定状态' or msg == '操作失败' or msg == '用户不存在':
        if msg == '帐号处于锁定状态' or msg == '用户不存在':
            logging.error(tag(msg))
            self.reason = config.REASON['account_forbidden']
            self.err = 1

    def successData(self):
        pass

    def createReq(self):
        pass

    def checkRepeat(self, resp):
        print(resp)
        msg = resp.json().get('msg')
        if msg is None:
            return
        if msg == '相同内容请间隔10分钟再进行发布哦！':
            self.err = 1
            self.reason = config.REASON['content_repeat']

def append_xsrf_header(st):
    header = copy.deepcopy(config.HEADER)
    header['X-XSRF-TOKEN'] = st
    return header

with open(config.COMMENTS_FILE, 'r',encoding='utf8') as f:
    comments = f.read()
    comments = list(comments)