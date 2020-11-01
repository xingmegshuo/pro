import rsa
import binascii
import re, random, json, time, logging, traceback, base64
import sinaRequests as requests
import http.cookiejar as cookielib

import config, utils
from . import BaseBot
from utils import tag
from verify import Verify
from bots import comments

# 个人信息
# https://m.weibo.cn/api/container/getIndex?type=uid&value=5846555329

class LoginBot(BaseBot):

    name = 'login'
    
    def __init__(self, taskid, params):
        super(LoginBot, self).__init__(taskid)
        self.username = str(params['username'])
        self.password = str(params['password'])
        self.is_checkip = params.get('checkip', None)
        self.proxy_id = params.get('proxy_id', None)
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar()
        self.verifyer = Verify()
        self.data = {
            'username': self.username,
            'password': self.password,
        }
        global LOGIN_UA, LOGIN_HEADER
        LOGIN_UA = random.choice(config.UA)
        LOGIN_HEADER = config.HEADER
        LOGIN_HEADER['User-Agent'] = LOGIN_UA


        # code：0，成功，
        # 1，网络错误，
        # 2，打码服务错误
        # 3、登陆错误
        # 4、帐号异常
        # 5、操作异常
        # 6、未知异常

    def crawl(self):
        if self.is_checkip:
            self.checkip()
        if self.code != 0:
            return
        resp = self.indexReq()
        time.sleep(random.randint(1, 3))
        success = self.login()
        if success:
            isban = None
            try:
                uid = self.data['uid']
                isban = self.checkmsg(uid)
            except expression as identifier:
                logging.info(tag('check msg err'))
            if isban is None:
                return
            self.code = 4
            return
        if self.code == 0:
            self.code = 6
            self.subcode = None

    def getPreloginInfo(self):
        url = ('http://login.sina.com.cn/sso/prelogin.php?'
            'entry=weibo&callback=sinaSSOController.preloginCallBack&'
            'su=&rsakt=mod&client=ssologin.js(v1.4.18)')
        self.url = 'http://login.sina.com.cn/sso/prelogin.php'
        self.response = None
        html = self.session.get(url).text
        self.response = html
        jsonStr = re.findall(r'\((\{.*?\})\)', html)[0]
        data = json.loads(jsonStr)
        return (data["servertime"], data["nonce"], data["pubkey"], 
            data["rsakv"], data['pcid'])

    def verify(self, pcid):
        url = 'https://login.sina.com.cn/cgi/pin.php'
        self.url = url
        self.response = None
        params = {
            'r': str(pcid),
            's': '0',
        }
        resp = self.session.get(url)
        code, self.subcode, self.url, self.response = self.verifyer.verify(resp.content,self.username)
        return code

    def login(self):
        # 登录并获取 crossDomainUrlList
        crossDomainUrlList = []
        servertime, nonce, pubkey, rsakv, pcid = self.getPreloginInfo()
        su = encodeUsername(self.username)
        sp = encodePassword(self.password, servertime, nonce, pubkey)
        code = self.verify(pcid)
        if code:
            resp = self.loginReq(nonce, rsakv, servertime, sp, su, code)
            logging.info(tag('login resp {resp}'.format(resp=resp.text)))
            data = resp.json()
            self.subcode = data['retcode']
            if 'reason' in data:
                reason = data['reason']
                if self.subcode == "2070":
                    logging.info(tag('输入的验证码不正确'))
                    self.code = 2
                    return
                if self.subcode == "101" or self.subcode=="2089":
                    logging.info(tag('登录名或密码错误'))
                    self.code = 3
                    return
                if self.subcode=="4010":
                    logging.info(tag('账号未激活'))
                    self.code = 3
                    return
            crossDomainUrlList = data['crossDomainUrlList']
        else:
            self.code = 2
            return
        # 请求 crossDomainUrlList
        # print('crossDomainUrlList', crossDomainUrlList)
        for cdcount, crossDomainUrl in enumerate(crossDomainUrlList):
            resp = self.session.get(crossDomainUrl, headers=LOGIN_HEADER)
            # with open('crossDomainUrl' + str(cdcount) + '.html', 'w') as  f:
            #     f.write(resp.text)

        # 判断是否跳转 https://weibo.com/nguide/recommend 推荐指南
        #self.process_recommend()

        # 跳转 m.weibo.cn
        _rand = str(time.time())
        params = {
            "url": "https://m.weibo.cn/",
            "_rand": _rand,
            "gateway": "1",
            "service": "sinawap",
            "entry": "sinawap",
            "useticket": "1",
            "returntype": "META",
            "sudaref": "",
            "_client_version": "0.6.29",
        }
        url = "https://login.sina.com.cn/sso/login.php"
        self.url = url
        self.response = None
        resp = self.session.get(url, params=params, headers=LOGIN_HEADER)
        resp.encoding = 'GBK'
        mres = re.findall(r'replace\((.*?)\);', resp.text)


        url = 'https://m.weibo.cn/api/config'
        self.url = url
        self.response = None
        resp = self.session.get(url, headers=LOGIN_HEADER)
        logging.debug(tag('config response: %s' % resp.text))
        data = resp.json()['data']
        if not data['login']:
            return
        uid, st = data['uid'], data['st']
        cookies = "#LWP-Cookies-2.0\n" + self.session.cookies.as_lwp_str()
        self.data = {
            'uid': uid,
            'st': st,
            'cookies': cookies,
            'username': self.username,
            'password': self.password,
            'ua': LOGIN_UA
        }
        return True

    def process_recommend(self):
        indexUrl = 'https://weibo.com'
        recommendUrl = 'https://weibo.com/nguide/recommend'
        resp = self.session.get(indexUrl)
        # with open('recommend.html', 'w') as  f:
        #     f.write(resp.text)
        # print (resp.text)
        print (resp.url)
        if not re.findall(recommendUrl, resp.url):
            logging.info(tag('no recommend'))
            return
        logging.info(tag('process recommend start'))
        nickname = gen_random_nickname()
        birthday = '-'.join([
            str(random.randint(1970, 2010)),
            str(random.randint(1, 12)),
            str(random.randint(1, 28))
        ])
        gender = random.choice(['f', 'm'])
        province = re.findall("CONFIG.city = '(\d+?)'", resp.text)
        city = re.findall("CONFIG.province = '(\d+?)'", resp.text)
        if (not province) or (not city):
            # 北京东城区
            province, city = ['11'], ['1']
        resp = registerReq(self.session, nickname, birthday, gender, 
            province[0], city[0])
        print (resp.url)
        print (resp.json())
        if not re.findall('/nguide/interests', resp.json()['data']):
            return
        interestsUrl = 'https://weibo.com/nguide/interests?backurl='
        resp = self.session.get(interestsUrl, headers=LOGIN_HEADER)
        # with open('interests.html', 'w') as  f:
        #     f.write(resp.text)
        data = gen_finish_data(resp)
        resp = finish4Req(self.session, data)
        print (resp.json())
        if resp.json().get('data', None):
            resp = self.session.get(resp.json()['data'])
            print (resp.url)

        # with open('finish4Req.html', 'w') as  f:
        #     f.write(resp.text)

    def checkmsg(self, uid):
        url = 'https://m.weibo.cn/profile/info?uid=' + uid
        self.url = 'https://m.weibo.cn/profile/info'
        self.response = None
        headers = {

        }
        resp = self.session.get(url)
        if re.findall('用户不存在', resp.text):
            self.subcode = 4001
            return True

        url = 'https://m.weibo.cn/message/msglist?page=1' # get uid
        self.url = url
        self.response = None
        resp = self.session.get(url)
        security_uid = None
        for i in resp.json()['data']:
            if i['user']['screen_name'] == '微博安全中心':
                security_uid = i['user']['id']
        if security_uid is None:
            logging.info(tag('no security msg'))
            return
        msgurl = 'https://m.weibo.cn/api/chat/list'
        self.url = msgurl
        self.response = None
        params = {
            'uid': security_uid,
            'count': 10,
            'unfollowing': 0,
        }
        resp = self.session.get(msgurl, params=params)
        verify_url = None
        # print(resp.json())
        for i in resp.json()['data']['msgs']:
            # 提取账户异常，解除异常的链接
            text = i['text']
            if not re.findall('帐号与安全提醒', text):
                continue
            verify_url = re.search('href=\\"(.*?)\\".*帐号与安全提醒', text)
            if verify_url:
                verify_url = verify_url.groups()[0]
        if verify_url is None:
            return
        resp = self.session.get(verify_url)
        resp.encoding = 'utf-8'
        if re.findall('为了解除帐号异常，请点击按钮进行验证', resp.text):
            self.subcode = 4002
            return True

    def checkip(self):
        # ip = requests.get('http://ddns.oray.com/checkip').text
        # ip = re.findall(r'Current IP Address: (.*?)</body>', ip)[0]
        ip = requests.get('http://whatismyip.akamai.com/').text
        logging.info(tag('ip: %s' % ip))
        params = {
            'ip': ip,
        }
        resp = requests.get(config.REPORT_IP_URL, params=params)
        print (resp.url)
        print (resp.text)
        is_continue = resp.json()['code']
        if int(is_continue) != 0:
            self.code = 1
            self.subcode = 1002

    def indexReq(self):
        url = 'https://m.weibo.cn/'
        self.url = url
        self.response = None
        resp = self.session.get(url, headers=LOGIN_HEADER)
        return resp

    def loginReq(self, nonce, rsakv, servertime, sp, su, code):
        url = 'https://login.sina.com.cn/sso/login.php'
        params = (
            ('client', 'ssologin.js(v1.4.15)'),
            ('_', '1542547431645'),
        )
        data = {
            "cdult" : "3",
            "domain" : "sina.com.cn",
            "encoding" : "UTF-8",
            "entry" : "account",
            "from" : "",
            "gateway" : "1",
            "nonce" : nonce,
            "pagerefer" : "http://my.sina.com.cn/profile/logined",
            "prelt" : "41",
            "pwencode" : "rsa2",
            "returntype" : "TEXT",
            "rsakv" : rsakv,
            "savestate" : "30",
            "servertime" : servertime,
            "service" : "sso",
            "sp" : sp,
            "sr" : "1366*768",
            "su" : su,
            "useticket" : "0",
            "vsnf" : "1",
            "door" : code,
            
            'qrcode_flag': True,
        }
        self.url = url
        resp = self.session.post(url, headers=LOGIN_HEADER, params=params, data=data)
        self.response = resp.json()
        logging.debug(tag('login req response: %s' % resp.text))
        return resp


def gen_finish_data(resp):
    datas = re.findall('tag_id="(\d+?:tagCategory_\d+)?" uids="([0-9,]+?)">', 
        resp.text)
    print(datas)
    datas = {k: v.split(',') for k, v in datas}
    print(datas)
    print('dataslength', len(datas))
    if len(datas) <= 5:
        return json.dumps(datas)
    index = random.randint(5, len(datas))
    print(index)
    print(json.dumps(dict(list(datas.items())[:index])))
    return json.dumps(dict(list(datas.items())[:index]))

def finish4Req(session, data):
    finish4url = 'https://weibo.com/nguide/aj/finish4'
    headers = {
        'Host': 'weibo.com',
        'Connection': 'keep-alive',
        'Origin': 'https://weibo.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': LOGIN_UA,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': 'https://weibo.com/nguide/interests?backurl=',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    data = {
        'data': data
    }
    resp = session.post(finish4url, data=data)
    return resp

def gen_random_nickname():
    length = random.randint(3, 12)
    return ''.join([random.choice(comments) for i in range(length)])


def registerReq(session, nickname, birthday, gender, province, city):
    register4url = 'https://weibo.com/nguide/aj/register4?__rnd=' + \
        str(utils.timestamp())
    headers = {
        'Host': 'weibo.com',
        'Connection': 'keep-alive',
        'Origin': 'https://weibo.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': LOGIN_UA,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': 'https://weibo.com/nguide/recommend?ugf=home',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    data = {
        'nickname': nickname,
        'birthday': birthday,
        'gender': gender,
        'province': province,
        'city': city,
        '_t': 0
    }
    resp = session.post(register4url, data=data, headers=headers)
    return resp


def encodeUsername(username):
    return base64.encodestring(username.encode('utf-8'))[:-1]

def encodePassword(password, servertime, nonce, pubkey):
    rsaPubkey = int(pubkey, 16)
    RSAKey = rsa.PublicKey(rsaPubkey, 65537)
    codeStr = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    pwd = rsa.encrypt(codeStr.encode('utf-8'), RSAKey)
    return binascii.b2a_hex(pwd)

if __name__ == '__main__':
    params = {
        'username': '23285yhuvippc@sina.com',
        'password': 'zipdd122'
    }
 

class FastLoginBot(LoginBot):

    name = 'fast_login'

class NormalLogin(LoginBot):

    name = 'normal_login'