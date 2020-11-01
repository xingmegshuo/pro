import time, random, logging, copy, re, json, traceback
import http.cookiejar as cookielib

import sinaRequests as requests
from bots import BaseBot
from utils import tag
import config



commentUrl = 'https://m.weibo.cn/api/comments/create'  #评论url
heartUrl = 'https://m.weibo.cn/api/attitudes/create'   #点赞url
repostUrl = 'https://m.weibo.cn/api/statuses/repost'   #回复url


class CustomizeBot(BaseBot):

    name = '_customize'

    def __init__(self, taskid, params):
        super(CustomizeBot, self).__init__(taskid)
        self.params = params

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
        datas = self.params['datas']
        blockresps = []
        self.data = {'datas': blockresps}
        for block in datas:
            block_data = {}
            blockid = block['blockid']
            params = block['params']
            block_data['blockid'] = blockid
            block_data['params'] = params
            block_data['actions'] = self.process_block(block)
            blockresps.append(block_data)
        self.reason = config.REASON['done']

    def process_block(self, block):
        actionsresp = {}
        params = block['params']
        actions = self.order_actions(block['actions'])
        uid = params['uid']
        st = params['st']
        cookies = params['cookies']
        session = self.initSession(uid, cookies)
        for action in actions:
            actionid = action.get('actionid')
            actype = action['type']
            acparams = action['params']
            funparams = copy.deepcopy(acparams)
            funparams['params'] = acparams
            funparams['session'] = session
            funparams['actype'] = actype
            funparams['st'] = st
            result = None
            try:
                result = process_fun[actype](**funparams)
            except:
                logging.error(tag('err run {actype}'.format(actype=actype)))
                logging.error(tag(traceback.format_exc()))
            if actionid:
                if result is None:
                    logging.error(tag('run {actype} result is None'.format(actype=actype)))
                    result = gen_report(actype, acparams, err=1, 
                        reason=config.REASON['bot_run_error'])
                actionsresp[str(actionid)] = result
        return actionsresp

    def order_actions(self, actions):
        actions_order = [None for i in range(len(actions))]
        order_index = [int(i) for i, _ in actions.items()]
        order_index.sort()
        for index, ackey in enumerate(order_index):
            ac = actions[str(ackey)]
            acid = ac.get('id')
            if acid:
                ac['actionid'] = acid
            actions_order[int(index)] = ac
        return actions_order

def sleep(**kwargs):
    millisecond = kwargs['millisecond']
    logging.info(tag('sleep: {millisecond}'.format(millisecond=millisecond)))
    if millisecond is None:
        time.sleep(random.uniform(1, 2))
        return
    time.sleep(int(millisecond) / 1000)

def weibo_index_req(**kwargs):
    session = kwargs['session']
    logging.info(tag('weibo_index_req'))
    url = 'https://m.weibo.cn/'
    resp = session.get(url, headers=config.HEADER)

def config_req(**kwargs):
    session = kwargs['session']
    logging.info(tag('config_req'))
    url = 'https://m.weibo.cn/api/config'
    resp = session.get(url, headers=config.HEADER)
    logging.info(tag('config_resp {resp}'.format(resp=resp.text)))


def heart_req(**kwargs):
    targetid = str(kwargs['targetid'])
    session = kwargs['session']
    params = kwargs['params']
    st = kwargs['st']
    actype = kwargs['actype']
    if check_blog_not_exist(session, targetid):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['blog_not_found'])
    data = {
        'id': targetid,
        'attitude': 'heart',
        'st': st,
    }
    logging.info(tag('heart_req {data}'.format(data=json.dumps(data))))
    resp = session.post(heartUrl, headers=config.HEADER, data=data)
    logging.info(tag('heart_resp {data}'.format(data=resp.text)))
    data = resp.json()
    msg = data.get('msg')
    ok = data.get('ok')
    if ok == 1:
        return gen_report(actype, params)
    if msg == '操作失败' or msg =='请求过于频繁,歇歇吧':
        return gen_report(actype, params, err=1, 
            reason=config.REASON['heart_operate_fail'])
    if check_acc_forbidden(msg):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['account_forbidden'])
    return gen_report(actype, params, err=1, 
        reason=config.REASON['bot_run_error'])

def comment_req(**kwargs):
    targetmid = str(kwargs['targetmid'])
    session = kwargs['session']
    params = kwargs['params']
    st = kwargs['st']
    actype = kwargs['actype']
    content = kwargs['content']
    if check_blog_not_exist(session, targetmid):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['blog_not_found'])
    data = {
        'content': content,
        'mid': targetmid,
        'st': st,
    }
    logging.info(tag('comment_req {data}'.format(data=json.dumps(data))))
    resp = session.post(commentUrl, headers=config.HEADER, data=data)
    logging.info(tag('comment_resp {data}'.format(data=resp.text)))
    data = resp.json()
    msg = data.get('msg')
    ok = data.get('ok')
    if ok == 1:
        return gen_report(actype, params)
    if msg == '发微博太多啦，休息一会儿吧!' or msg =='请求过于频繁,歇歇吧':
        return gen_report(actype, params, err=1, 
            reason=config.REASON['frequent_comment'])
    if check_repeat(msg):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['content_repeat'])
    if check_acc_forbidden(msg):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['account_forbidden'])
    return gen_report(actype, params, err=1, 
        reason=config.REASON['bot_run_error'])

def repost_req(**kwargs):
    session = kwargs['session']
    params = kwargs['params']
    targetid = str(kwargs['targetid'])
    targetmid = str(kwargs['targetmid'])
    content = kwargs['content']
    dualPost = 1 if kwargs['dualPost'] else 0
    actype = kwargs['actype']
    st = kwargs['st']
    if check_blog_not_exist(session, targetid):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['blog_not_found'])
    data = {
        'id': targetid,
        'content': content if content else '转发微博',
        'dualPost': dualPost,
        'mid': targetmid,
        'st': st,
    }
    logging.info(tag('respost_req {data}'.format(data=json.dumps(data))))
    resp = session.post(repostUrl, headers=config.HEADER, data=data)
    logging.info(tag('repost_resp {data}'.format(data=resp.text)))

    data = resp.json()
    msg = data.get('msg')
    ok = data.get('ok')
    if ok == 1:
        return gen_report(actype, params)
    if msg == '发微博太多啦，休息一会儿吧!' or msg =='请求过于频繁,歇歇吧':
        return gen_report(actype, params, err=1, 
            reason=config.REASON['frequent_repost'])
    if check_repeat(msg):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['content_repeat'])
    if check_acc_forbidden(msg):
        return gen_report(actype, params, err=1, 
            reason=config.REASON['account_forbidden'])
    return gen_report(actype, params, err=1, 
        reason=config.REASON['bot_run_error'])



# def read_blog_req(session=None,  st=None, params=None, type=None, **kwargs):
#     pass


def gen_report(actype, params, err=0, reason=config.REASON['done']):
    return {
        'type': actype,
        'err': err,
        'data': params,
        'reason': reason
    }

def check_blog_not_exist(session, mid):
    url = 'https://m.weibo.cn/detail/' + mid
    resp = session.get(url, headers=config.HEADER)
    if re.findall(r'微博不存在或暂无查看权限!', resp.text):
        return True

def check_repeat(msg):
    if msg == '相同内容请间隔10分钟再进行发布哦！':
        return True

def check_acc_forbidden(msg):
    # 点赞任务：账户被封、目标博文不存在 msg 都为'操作失败'
    # 关注任务：账户被封、目标用户不存在 msg 都为'用户不存在'
    # 对于这个两个任务，执行之前会提前访问博文页或用户页检测是否存在，
    # 执行任务之后，运行到此函数是，再返回 '操作失败'、'用户不存在'，则判定为账户被封

    # 修改：去除对点赞返回 操作失败的检查，对于这种情况不在判断为账户异常，
    # 而是返回新的错误类型，避免账户状态的误判，因为短时间内点赞超过 15 次，也会返回操作失败
    if msg == '帐号处于锁定状态' or msg == '用户不存在':
        return True



process_fun = {
    'sleep': sleep,
    'weibo_index_req': weibo_index_req,
    # 'config_req': config_req,
    'repost_req': repost_req,
    'heart_req': heart_req,
    'comment_req': comment_req,
}



# {
#     "code":0,
#     "message":"操作成功",
#     "data":{
#         "taskid":1543563816,
#         "type":"customize",
#         "timeout":300,
#         "params":{
#             "datas":[
#                 {
#                     "blockid":"123",
#                     "params":{
#                         "uid":"..",
#                         "st":"..",
#                         "cookies":".."
#                     },
#                     "actions":{
#                         "1":{
#                             "type":"read_weibo_index",
#                             "param":{

#                             }
#                         },
#                         "2":{
#                             "type":"sleep",
#                             "param":{
#                                 "millisecond":1500
#                             }
#                         },
#                         "3":{
#                             "id":1123,
#                             "type":"comment",
#                             "params":{
#                                 "targetmid":4328516705121537,
#                                 "content":"comment test..."
#                             }
#                         },
#                         "4":{
#                             "id":1123,
#                             "type":"repost",
#                             "params":{
#                                 "targetid":4328516705121537,
#                                 "targetmid":4328516705121537,
#                                 "content":"",
#                                 "dualPost":false
#                             }
#                         },
#                         "5":{
#                             "id":1123,
#                             "type":"heart",
#                             "params":{
#                                 "targetid":4328516705121537
#                             }
#                         }
#                     }
#                 }
#             ]
#         }
#     }
# }

# {
#     "taskid":1543563816,
#     "type":"customize",
#     "err":0,
#     "data":{
#         "datas":[
#             {
#                 "blockid":12312312,
#                 "params":{
#                   "uid":"..",
#                   "st":"..",
#                   "cookies":".."
#                 },
#                 "actions":{
#                     "action_id-0":{
#                         "type":"comment",
#                         "err":0,
#                         "data":{
#                             "targetmid":4328516705121537,
#                             "content":"comment test..."
#                         },
#                         "reason":"done"
#                     },
#                     "action_id-1":{
#                         "type":"repost",
#                         "err":1,
#                         "data":{
#                             "targetid":4328516705121537,
#                             "targetmid":4328516705121537,
#                             "content":"",
#                             "dualPost":false
#                         },
#                         "reason":"content_repeat"
#                     },
#                     "action_id-2":{
#                         "type":"heart",
#                         "err":0,
#                         "data":{
#                             "targetid":4328516705121537
#                         },
#                         "reason":"done"
#                     }
#                 }
#             }
#         ]
#     },
#     "reason":"done"
# }


# {
#     "taskid": 1543563816,
#     "type": "customize",
#     "err": 0,
#     "data": {
#         "datas": [
#             {
#                 "blockid": "1",
#                 "params": {
#                     "uid": "6999832666",
#                     "st": "95d8f2",
#                     "cookies": "#LWP-Cookies-2.0\nSet-Cookie3: ALF=1555318576; path=\"/\"; domain=\".97973.com\"; path_spec; domain_dot; expires=\"2019-04-15 08:56:16Z\"; version=0\nSet-Cookie3: SSOLoginState=1552726576; path=\"/\"; domain=\".97973.com\"; path_spec; discard; version=0\nSet-Cookie3: ALC=\"ac%3D2%26bt%3D1552726576%26cv%3D5.0%26et%3D1584262576%26ic%3D1875241599%26login_time%3D1552726575%26scf%3D%26uid%3D6999832666%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D87e5ace38540083e9a1c9d5a1445c17a\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; expires=\"2020-03-15 08:56:16Z\"; httponly=None; version=0\nSet-Cookie3: LT=1552726576; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: tgc=\"TGT-Njk5OTgzMjY2Ng==-1552726576-tc-513083292836BE8DE1D0886F260731CF-1\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; Httponly=None; version=0\nSet-Cookie3: SRF=1552726576; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-03-13 08:56:16Z\"; version=0\nSet-Cookie3: SRT=\"D.QqHBJZPtT4snSrMb4cYGS4HziFoqdZYu5!kwPGEHNEYd4s035dypMERt4EPKRcsrA4kJPcHsTsVuObESN!Ho5coPRqBLdOHTAcoOPOHE4OB94!WIPFEZO3Br*B.vAflW-P9Rc0lR-ykTDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPVsU44rJPyBTcPzOPED4-f3Q-kDRro-i49ndDPIJcYPSrnlMcyoiDEIIbHbJG9Z4-yoJcM1OFyHi3bgVdWJT-4n5ZBOAeMr\"; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-03-13 08:56:16Z\"; httponly=None; version=0\nSet-Cookie3: ALF=1584262576; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; version=0\nSet-Cookie3: SCF=\"AoCMllYbFAgKSg6ePobtxDtcsSjqINzCDRawm4azXELkF2mjJIYD9xx00j7vHg8NlbzugoUnobVabUtuCYGlN3k.\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2029-03-13 08:56:16Z\"; httponly=None; version=0\nSet-Cookie3: SUB=_2A25xiMpgDeRhGeBH4lsZ8yzKzTqIHXVTctYorDV_PUJbm9AKLVPNkW1NQYJBq3ceGjY0dfmHgOY6MfwqQXFR4U7L; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5mE41_AjeHMQCSj7_kCcLv5NHD95Qc1K.41heESoqcWs4Dqcjzds8DP0eEe0-t\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: ULOGIN_IMG=\"tc-de8f79741ddf1587ff385ef2c58523c22571\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: sso_info=\"v02m6alo5qztayYlqWfjLOIs42SmbWalpC9jaOkuY6ToLOMo5i2jaDAwA==\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-03-16 08:56:16Z\"; version=0\nSet-Cookie3: ALF=1555318576; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-04-15 08:56:16Z\"; version=0\nSet-Cookie3: MLOGIN=1; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-03-16 09:56:17Z\"; version=0\nSet-Cookie3: M_WEIBOCN_PARAMS=\"luicode%3D20000174\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-03-16 09:06:17Z\"; HttpOnly=None; version=0\nSet-Cookie3: SCF=\"AoCMllYbFAgKSg6ePobtxDtcsSjqINzCDRawm4azXELkF2mjJIYD9xx00j7vHg8Nla4fXdj6fTzN-gS8BdlBwzo.\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2029-03-13 08:56:16Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1552726576; path=\"/\"; domain=\".weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: SUB=_2A25xiMpgDeRhGeBH4lsZ8yzKzTqIHXVTctYorDV6PUJbktAKLVWkkW1NQYJBq45zPofX1JYvVW0bwN6BAb13XXpI; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5mE41_AjeHMQCSj7_kCcLv5JpX5K-hUgL.Foq41K.Re0zcSoq2dJLoI7yjqgLke0z0SBtt\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; version=0\nSet-Cookie3: SUHB=06ZVzNH1gRq2MJ; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; version=0\nSet-Cookie3: WEIBOCN_FROM=1110005030; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: XSRF-TOKEN=287a7c; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: _T_WM=eb6afe83b3e77e27ac8a8df40a076259; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-04-15 08:56:12Z\"; version=0\nSet-Cookie3: ALF=1584262576; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; version=0\nSet-Cookie3: SCF=\"AoCMllYbFAgKSg6ePobtxDtcsSjqINzCDRawm4azXELkF2mjJIYD9xx00j7vHg8NlaiKWzVqQluDMZOPe1ZhOrk.\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2029-03-13 08:56:16Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1552726576; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: SUB=_2A25xiMpgDeRhGeBH4lsZ8yzKzTqIHXVS_7yorDV8PUNbmtAKLVbukW9NQYJBqzlUc0OY2ZBlSU2EQ0iRGKTacOpt; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5mE41_AjeHMQCSj7_kCcLv5JpX5K2hUgL.Foq41K.Re0zcSoq2dJLoI7yjqgLke0z0SBtt\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; version=0\nSet-Cookie3: SUHB=0oU4yVvBIaxUQo; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-03-15 08:56:16Z\"; version=0\nSet-Cookie3: login=ec1b2ebb0879ca371fdf54d7c71fe5fa; path=\"/\"; domain=\"login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=2539a3746215f32d05c8100e941e1569; path=\"/\"; domain=\"passport.97973.com\"; path_spec; discard; version=0\nSet-Cookie3: login=2539a3746215f32d05c8100e941e1569; path=\"/\"; domain=\"passport.weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=13a0857768fc0c0abafd3d70c0f4538a; path=\"/\"; domain=\"passport.weibo.com\"; path_spec; discard; version=0\n"
#                 },
#                 "actions": {
#                     "1": {
#                         "type": "comment_req",
#                         "err": 0,
#                         "data": {
#                             "targetmid": 4350173197316243,
#                             "content": "后"
#                         },
#                         "reason": "done"
#                     },
#                     "2": {
#                         "type": "repost_req",
#                         "err": 0,
#                         "data": {
#                             "targetid": 4350173197316243,
#                             "targetmid": 4350173197316243,
#                             "content": "",
#                             "dualPost": false
#                         },
#                         "reason": "done"
#                     },
#                     "3": {
#                         "type": "heart_req",
#                         "err": 0,
#                         "data": {
#                             "targetid": 4350173197316243
#                         },
#                         "reason": "done"
#                     }
#                 }
#             }
#         ]
#     },
#     "reason": "done"
# }