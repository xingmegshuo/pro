import time, random, logging, copy, re, json, traceback
import http.cookiejar as cookielib
import sinaRequests as requests
from bots import BaseBot
from utils import tag
import config
from . import configUrl
from bots.actions.sleep import Sleep
from bots.actions.heart_req import HeartReq
from bots.actions.comment_req import CommentReq
from bots.actions.repost_req import RepostReq
from bots.actions.weibo_index_req import WeiboIndexReq
from bots.actions.friendship_req import FriendshipReq
from bots.actions.update_req import UpdateReq
funs = [Sleep, HeartReq, CommentReq, RepostReq, WeiboIndexReq, FriendshipReq, UpdateReq]
process_fun = {fun.name: fun for fun in funs}




class CustomizeBot(BaseBot):

    name = 'customize'

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

    def isExpired(self, session):
        resp = session.get(configUrl, headers=config.HEADER)
        logging.info(tag('config response: %s' % resp.text))
        data = resp.json()['data']
        st = None
        if data['login']:
            st = data['st']
        return st, resp.json()

    def crawl(self):
        datas = self.params['datas']
        blockresps = []
        self.data = {'datas': blockresps}
        for block in datas:
            block_data = {}
            blockid = block['blockid']
            params = block['params']
            block_data['blockid'] = blockid
            block_data['params'] = {'uid': params['uid']}
            block_data['actions'] = self.process_block(block)
            blockresps.append(block_data)
        self.reason = config.REASON['done']

    def process_block(self, block):
        code, subcode = 0, None
        actionsresp = {}
        params = block['params']
        actions = self.order_actions(block['actions'])
        uid = params['uid']
        st = params['st']
        ua = params['ua']
        cookies = params['cookies']
        session = self.initSession(uid, cookies)
        reason = None
        # TODO
        st, response = self.isExpired(session)
        if st is None:
            url = configUrl
            response = response
            code = 4
            subcode = 4003
            return
        for action in actions:
            actionid = action.get('actionid')
            actype = action['type']
            acparams = action['params']
            funparams = copy.deepcopy(acparams)
            if code != 0:
                actionsresp[str(actionid)] = {
                    'taskid': actionid,
                    'type': actype,
                    'code': code,
                    'subcode': subcode,
                    'url': url,
                    'response': response,
                    'data': {},
                }
                continue
            processor = process_fun[actype](session, ua, uid, st)
            result = processor.run(**funparams)
            result['taskid'] = actionid
            showWorkerResult(result)
            del result['traceback_info']
            actionsresp[str(actionid)] = result
        return actionsresp

    def order_actions(self, actions):
        actions_order = [None for i in range(len(actions))]
        order_index = [int(i) for i, _ in actions.items()]
        order_index.sort()
        for index, ackey in enumerate(order_index):
            ac = actions[str(ackey)]
            # acid = ac.get('id')
            # if acid:
            ac['actionid'] = str(ackey)
            actions_order[int(index)] = ac
        return actions_order

def showWorkerResult(result):
    logging.info(tag('worker result:'))
    for title, info in result.items():
        logging.info(tag('      %s:%s' % (title, info)))

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