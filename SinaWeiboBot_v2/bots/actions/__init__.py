import copy, traceback, re, os
import utils
from config import REASON
from config import HEADER

class ActionBase(object):
    name = None
    def __init__(self, session, ua, uid, st):
        self.session = session
        self.headers = copy.deepcopy(HEADER)
        self.ua = ua
        self.headers['User-Agent'] = ua
        self.uid = uid
        self.st = st
        self.cachefiles = []

    def run(self, *args, **kwargs):
        code, subcode, url, response, data = 0, None, None, None, {}
        start_at = utils.timestamp()
        traceback_info = None
        try:
            code, subcode, url, response, data = self.crawl(*args, **kwargs)
        except:
            traceback_info = traceback.format_exc()
            code = 6
        finished_at = utils.timestamp()
        data['start_at'] = start_at
        data['finished_at'] = finished_at
        data['uid'] = self.uid
        result = {
            'type': self.name,
            'code': code,
            'data': data,
            'traceback_info': traceback_info,
        }
        if subcode:
            result['subcode'] = subcode
        if url:
            result['url'] = url
        if response and code != 0:
            result['response'] = response

        for i in self.cachefiles:
            if os.path.exists(i):
                os.remove(i)
        return result

    def crawl(self):
        pass

    def parse_resp(self, data):
        msg = data.get('msg')
        ok = data.get('ok')
        code, subcode = 0, data.get('errno')
        if ok == 1:
            return code, subcode
        code, subcode2 = self.check_msg(msg)
        if subcode2:
            subcode = subcode2
        return code, subcode

    def check_msg(self, msg):
        # TODO config 接口也要判断这个 msg
        if msg == '请求过于频繁,歇歇吧':
            return 5, None
        if msg == 'token校验失败':
            return 4, None
        if msg == '由于作者隐私设置，你没有权限评论此微博':
            return 5, None
        if msg == '抱歉，根据相关法律法规的要求，此内容无法发布。':
            return 5, None
        if msg == '帐号处于锁定状态':
            return 4, 4002
        if msg == '用户不存在':
            return 4, 4001
        if msg == '相同内容请间隔10分钟再进行发布哦！':
            return 5, None
        if msg == '操作失败':
            return 5, None
        if msg == '发微博太多啦，休息一会儿吧!':
            return 5, None
        if msg == '作者只允许粉丝评论!':
            return 5, None
        return 6, None

    def check_blog_not_exist(self, mid):
        url = 'https://m.weibo.cn/detail/' + str(mid)
        resp = self.session.get(url, headers=self.headers)
        if re.findall(r'微博不存在或暂无查看权限!', resp.text):
            return 5001
        if re.findall(r'由于作者隐私设置，你没有权限查看此微博', resp.text):
            return 5003

    def check_user(self, uid):
        url = 'https://m.weibo.cn/profile/info?uid=' + str(uid)
        resp = self.session.get(url, headers=self.headers)
        if re.findall('用户不存在', resp.text):
            self.subcode = 5004
            return True