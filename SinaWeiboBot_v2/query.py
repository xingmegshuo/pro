#coding=utf-8
import json
import tornado.ioloop
import tornado.web
from tornado.web import Application, StaticFileHandler
import sinaRequests as requests
logindata = {"taskid": 1543563816, "type": "login", "err": 0, "data": {"uid": "5846555329", "st": "6d95a8", "cookies": "#LWP-Cookies-2.0\nSet-Cookie3: ALF=1559391894; path=\"/\"; domain=\".97973.com\"; path_spec; domain_dot; expires=\"2019-06-01 12:24:54Z\"; version=0\nSet-Cookie3: SSOLoginState=1556799894; path=\"/\"; domain=\".97973.com\"; path_spec; discard; version=0\nSet-Cookie3: ALC=\"ac%3D2%26bt%3D1556799893%26cv%3D5.0%26et%3D1588335893%26ic%3D-562032854%26login_time%3D1556799893%26scf%3D%26uid%3D5846555329%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D8ceb5bc7bab665f1260974d6b2252b2f\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; expires=\"2020-05-01 12:24:53Z\"; httponly=None; version=0\nSet-Cookie3: LT=1556799894; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: tgc=\"TGT-NTg0NjU1NTMyOQ==-1556799893-tc-99D53EEB9D6B3A36884044D8D416D26B-1\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; Httponly=None; version=0\nSet-Cookie3: XSRF-TOKEN=6d95a8; path=\"/\"; domain=\".m.weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: SRF=1556799893; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-04-29 12:24:53Z\"; version=0\nSet-Cookie3: SRT=\"D.QqHBJZPt5eBzM!Mb4cYGS4uGiqEMPObOWbBuPEWHNEYd43SS44upMERt4EPKRcsrA4kJProQTsVuObJnPrybW-bn4398TdHfMFHJWeiMM-PqJFymMF9u4Q4q*B.vAflW-P9Rc0lR-yk!DvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWfIOmp5EYdJ!MPKF9!TsBoW!A-RrEpi49ndDPIJcYPSrnlMc0k4bifVdSONprnSd0lJcM1OFyHMQEJ5mjkOmHII4oCI!HJ5mkCOmzlJ!oCIZHJ5mjlOmHIJ!oCIZHJ5mjlOmHIJ!oCIZHK4qWrWv77\"; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-04-29 12:24:53Z\"; httponly=None; version=0\nSet-Cookie3: ALF=1588335893; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:53Z\"; version=0\nSet-Cookie3: SCF=\"AqjrE9D7jjYuaQrA9dPUhwEO_eFpnecoHnWlbhTfgBFUibDMj_0f9_TT_kuWf6OFQQcl8K2qFCy4DWNeuZEvzb0.\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2029-04-29 12:24:53Z\"; httponly=None; version=0\nSet-Cookie3: SUB=\"_2A25xzpHGDeRhGeNG71QU9SvPyTWIHXVTMD-OrDV_PUJbm9AKLU39kW1NS0WOe4WwDWAEWqRXndtCiZ75nkiP5FUP\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:54Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-12xXV2DU8jdkPqvD6cAr5NHD95Qf1hBcSK-fe0z4Ws4DqcjJi--fi-2fi-i2i--Xi-iWi-iWi--4i-2pi-iWi--4i-2pi-iWS0Mt\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: ULOGIN_IMG=\"tc-d3f5002d403850f8f95bc6dcdef1a598d614\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: sso_info=\"v02m6alo5qztKWRk5SlkJOUpZCkkKWRk5ClkKSEpZCkhKWRk6SlkJOEpZCkhKWRk6SlkJOEpZCkhLeNspm1mpaQvY2ToLSNo5S1jZOMso6QwMA=\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-02 12:24:53Z\"; version=0\nSet-Cookie3: ALF=1559391894; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-06-01 12:24:54Z\"; version=0\nSet-Cookie3: MLOGIN=1; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-02 13:24:54Z\"; version=0\nSet-Cookie3: M_WEIBOCN_PARAMS=\"luicode%3D20000174\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-02 12:34:54Z\"; HttpOnly=None; version=0\nSet-Cookie3: SCF=\"AqjrE9D7jjYuaQrA9dPUhwEO_eFpnecoHnWlbhTfgBFUV3cUlvwZ25DMOGP2FMTXFYqYZwPuPIlKIJLQLHCxoak.\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2029-04-29 12:24:54Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1556799894; path=\"/\"; domain=\".weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: SUB=\"_2A25xzpHGDeRhGeNG71QU9SvPyTWIHXVTMD-OrDV6PUJbktAKLULskW1NS0WOe1mYtD-UpL9MZiYCtQQSf74d8cqu\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:54Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-12xXV2DU8jdkPqvD6cAr5JpX5K-hUgL.Fo-RShqfSK-0eo.2dJLoIEqLxK-LBK-LB.BLxKBLB.2LB.2LxK.LBK2LB.2LxK.LBK2LB.2NS7tt\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:54Z\"; version=0\nSet-Cookie3: SUHB=0BLYG47hKQVVLw; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:54Z\"; version=0\nSet-Cookie3: WEIBOCN_FROM=1110003030; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: _T_WM=52442837956; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-12 12:24:47Z\"; version=0\nSet-Cookie3: ALF=1588335893; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:54Z\"; version=0\nSet-Cookie3: SCF=\"AqjrE9D7jjYuaQrA9dPUhwEO_eFpnecoHnWlbhTfgBFUibDMj_0f9_TT_kuWf6OFQU-elg5qNMZ0F2sa2rLkEuM.\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2029-04-29 12:24:53Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1556799893; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: SUB=_2A25xzpHFDeRhGeNG71QU9SvPyTWIHXVSvYQNrDV8PUNbmtAKLWLWkW9NS0WOewipSzbibhDbLvsQGes0oDDjyQu3; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-12xXV2DU8jdkPqvD6cAr5JpX5K2hUgL.Fo-RShqfSK-0eo.2dJLoIEqLxK-LBK-LB.BLxKBLB.2LB.2LxK.LBK2LB.2LxK.LBK2LB.2NS7tt\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:53Z\"; version=0\nSet-Cookie3: SUHB=0ElqIlOH6gFK3Q; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-01 12:24:53Z\"; version=0\nSet-Cookie3: login=f656a41107fa6197509ed6d05b9390fd; path=\"/\"; domain=\"login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=a902e3917463c16c83238d20c9245191; path=\"/\"; domain=\"passport.97973.com\"; path_spec; discard; version=0\nSet-Cookie3: login=13a0857768fc0c0abafd3d70c0f4538a; path=\"/\"; domain=\"passport.weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=ec1b2ebb0879ca371fdf54d7c71fe5fa; path=\"/\"; domain=\"passport.weibo.com\"; path_spec; discard; version=0\n", "username": "18001167287", "password": "shamao123", "start_at": 1556799887911, "finished_at": 1556799894674}, "reason": "done"}

# logindata = {
#   "taskid": 1543563816,
#   "type": "login",
#   "data": {
#     "uid": "7050711121",
#     "st": "57a05f",
#     "cookies": "#LWP-Cookies-2.0\nSet-Cookie3: ALF=1560684700; path=\"/\"; domain=\".97973.com\"; path_spec; domain_dot; expires=\"2019-06-16 11:31:40Z\"; version=0\nSet-Cookie3: SSOLoginState=1558092700; path=\"/\"; domain=\".97973.com\"; path_spec; discard; version=0\nSet-Cookie3: ALC=\"ac%3D27%26bt%3D1558092694%26cv%3D5.0%26et%3D1589628694%26ic%3D2099346489%26login_time%3D1558092694%26scf%3D%26uid%3D7050711121%26vf%3D1%26vs%3D0%26vt%3D4%26es%3Dc1c6e8220f342ef2344afb793249b7e6\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; expires=\"2020-05-16 11:31:34Z\"; httponly=None; version=0\nSet-Cookie3: LT=1558092705; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: tgc=\"TGT-NzA1MDcxMTEyMQ==-1558092694-tc-F06B99CBA8926ABDC63018B1AD32F17A-1\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; Httponly=None; version=0\nSet-Cookie3: XSRF-TOKEN=57a05f; path=\"/\"; domain=\".m.weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: SRF=1558092695; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-05-14 11:31:35Z\"; version=0\nSet-Cookie3: SRT=\"D.QqHBJZPtJeP-M!Mb4cYGS4SLi-oHPqYOQruuPDHHNEYd43HjUrupMERt4EPKRcsrA4kJ4!MdTsVuObERM4b-NOEoROYH5mWOR-nsQ-yQKmMwPcVoAdkhIduY*B.vAflW-P9Rc0lR-ykhDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWQT4igAqEBSZJkA3YlJq!nMsbm43P1i49ndDPIJcYPSrnlMcyiisiIi4ubNqHnSd0pJcM1OFyHJDWJ5mkiOmH6A!oCIQEJ5mkCOmzlJ!noTGEJ5mklOmH6I4oCUqPJ5mkCOmzlJ!noTGEJ5mkoODEII4oCN-PJ5mkCOmzlJ!noTD!tNm9SR-PIJeA7\"; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-05-14 11:31:35Z\"; httponly=None; version=0\nSet-Cookie3: ALF=1589628694; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:34Z\"; version=0\nSet-Cookie3: SCF=\"AvK-8abyOVp38VfJ5xh7bbUgu4KkRk2LnyFdAmNJlG8pYkw5SVSt2wI1yj92jAuUg0Z2awKHACdWZVtw_zh36II.\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2029-05-14 11:31:34Z\"; httponly=None; version=0\nSet-Cookie3: SUB=_2A25x2uvxDeRhGeFO7lIW8S_NyT2IHXVTJPW5rDV_PUJbm9AKLVXVkW1NQXEIvFRDFJmuIq3coKqJ6z2SLoo9ftE3; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:45Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9WWiCjC1Af3-Cxn390GYDSuJ5NHD95QNeh-7S02peKzpWs4DqcjYi--Ni-zXi-8si--Xi-iWiKnci--Ri-zfi-z7i--Xi-iWiKnci--ciK.fi-20i--Xi-iWiKncxH9aSo2p\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: ULOGIN_IMG=\"tc-a827c2cae9a278674fa8632db58c5f9fb889\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: sso_info=v02m6alo5qztKWRk5ylkKOQpZCUmKWRk5ClkKSEpY6DmKWRk6ClkKOUpZCjgKWRk5ClkKSEpY6DmKWRk5iljpOUpZCTjKWRk5ClkKSEpY6DmYWVpry2jJOEpp2WpaSPk5ywjZOAt4yThLGMo4TA; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-17 11:31:34Z\"; version=0\nSet-Cookie3: ALF=1560684705; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-06-16 11:31:45Z\"; version=0\nSet-Cookie3: MLOGIN=1; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-17 12:31:46Z\"; version=0\nSet-Cookie3: M_WEIBOCN_PARAMS=\"luicode%3D20000174\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-17 11:41:46Z\"; HttpOnly=None; version=0\nSet-Cookie3: SCF=\"AvK-8abyOVp38VfJ5xh7bbUgu4KkRk2LnyFdAmNJlG8prqIe1LTQnU2t8obGmjYmmKeSThxEjQOxIocgHbPx4II.\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2029-05-14 11:31:46Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1558092706; path=\"/\"; domain=\".weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: SUB=\"_2A25x2uvyDeRhGeFO7lIW8S_NyT2IHXVTJPW6rDV6PUJbktAKLRPikW1NQXEIvHFcnYnRD7gMTR1FE-lVql24eHD3\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:46Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9WWiCjC1Af3-Cxn390GYDSuJ5JpX5K-hUgL.FoM7SK5NeK2peo22dJLoI07LxKMLBoBLB-qLxKBLB.2L1hqLxKnLBo-LBo5LxKBLB.2L1hqLxKqL1K-LBKeLxKBLB.2L1h98HJYceK2t\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:46Z\"; version=0\nSet-Cookie3: SUHB=0ft5FxCsOa0Ia3; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:46Z\"; version=0\nSet-Cookie3: WEIBOCN_FROM=1110003030; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: _T_WM=65676553295; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-27 11:31:18Z\"; version=0\nSet-Cookie3: ALF=1589628694; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:34Z\"; version=0\nSet-Cookie3: SCF=\"AvK-8abyOVp38VfJ5xh7bbUgu4KkRk2LnyFdAmNJlG8pTD9luJ0uzOHAgxk759w5rE5x4U1bBRT0ZFlZ47jrzlU.\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2029-05-14 11:31:35Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1558092695; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: SUB=\"_2A25x2uvFDeRhGeFO7lIW8S_NyT2IHXVSrloNrDV8PUNbmtAKLRDVkW9NQXEIvI1qa8IxGScl5_oW8DzVg1Akk-na\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9WWiCjC1Af3-Cxn390GYDSuJ5JpX5K2hUgL.FoM7SK5NeK2peo22dJLoI07LxKMLBoBLB-qLxKBLB.2L1hqLxKnLBo-LBo5LxKBLB.2L1hqLxKqL1K-LBKeLxKBLB.2L1h98HJYceK2t\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:35Z\"; version=0\nSet-Cookie3: SUHB=0mxErNbhKccuiQ; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-16 11:31:35Z\"; version=0\nSet-Cookie3: login=ec1b2ebb0879ca371fdf54d7c71fe5fa; path=\"/\"; domain=\"login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=a902e3917463c16c83238d20c9245191; path=\"/\"; domain=\"passport.97973.com\"; path_spec; discard; version=0\nSet-Cookie3: login=f656a41107fa6197509ed6d05b9390fd; path=\"/\"; domain=\"passport.weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=f656a41107fa6197509ed6d05b9390fd; path=\"/\"; domain=\"passport.weibo.com\"; path_spec; discard; version=0\n",
#     "username": "1553624sy0lo@qt005.cc",
#     "password": "YZUzda561Qs",
#     "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
#     "start_at": 1558092677646,
#     "finished_at": 1558092712423
#   },
#   "code": 4,
#   "subcode": 4002,
#   "url": "https://m.weibo.cn/api/chat/list"
# }

uid = logindata['data']['uid']
st = logindata['data']['st']
cookies = logindata['data']['cookies']

taskPv = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "pv",
    "timeout": 300,
    "params": {
      "targeturl": "https://weibo.com/6829531006/HbUbUfsch",
      # "targeturl": "https://weibo.com/5846555329/HcODpoMWh",
      "count": 100
    }
  }
}
taskBlog = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "blog",
    "timeout": 3000,
    "params": {
      "uid": 1826792401,
      # "uid": 5764930318,
      "lastdate": None,
      # "lastdate": "2018-10-01"
    }
  }
}
loginTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "login",
    "timeout": 3000,
    "params": {
      "checkip": True,
      "username": "18001167287",
      "password": "shamao123",
      # "password": "123123123",
      # "username": "yidangbai9bd@163.com",
      # "password": "FHEwgt291vb"
      "username": "1553624sy0lo@qt005.cc",
      "password": "YZUzda561Qs",
    }
  }
}

heartTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "heart",
    "timeout": 3000,
    "params": {
      "targetid": 4364881215462804,
      # "targetid": 4330539735212312,
      "st": st,
      "uid": uid,
      "cookies": cookies,
    }
  }
}

fastheartTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "fast_heart",
    "timeout": 3000,
    "params": {
      "targetid": 4340385385979700,
      # "targetid": 4330539735212312,
      "st": st,
      "uid": uid,
      "cookies": cookies,
    }
  }
}

repostTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "repost",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,

      # 'targetid': 43283977207812312,
      # 'targetmid': 4328397720712312,
                                "targetid":4350173197316243,
                                "targetmid":4350173197316243,
                                "content":"",
                                "dualPost":False
    }
  }
}
fastrepostTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "fast_repost",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,

      # 'targetid': 43283977207812312,
      # 'targetmid': 4328397720712312,
      'targetid': 4341357373296665,
      'targetmid': 4341357373296665,
      'content': '嘿嘿',
      'dualPost': True,
    }
  }
}


friendshipTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "friendship",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,

      "targetuid": 5846555329,
      # "targetuid": 123123,
    }
  }
}

commentTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "comment",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,

      'targetmid': 4365018465808024,
      'content': 'comment test...',
    }
  }
}

fastCommentTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "fast_comment",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,

      'targetmid': 4342088890271041,
      'content': 'comment test...',
    }
  }
}


updateTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "update",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,

      "content": "update test",
    }
  }
}

updateEnvTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "updateEnv",
    "timeout": 3000,
    "params": {
      "sh": "sleep 5\npwd\nls -al",
    }
  }
}

updateBotTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "updateBot",
    "timeout": 3000,
    "params": {
      "bot": "testBot.py",
      "content": "#coding=utf-8\nimport logging\nimport sinaRequests as requests\nimport config\nfrom . import CreateBaseBot\n\n\nheartUrl = 'https://m.weibo.cn/api/attitudes/create'\n\nclass HeartBot(CreateBaseBot):\n\n    name = 'test'\n    \n    def __init__(self, taskid, childPipe, params):\n        cookies = params['cookies']\n        uid = str(params['uid'])\n        self.st = params['st']\n        super(HeartBot, self).__init__(taskid, childPipe, uid, cookies)\n        self.targetid = str(params['targetid'])\n\n    def createReq(self):\n        data = {\n            'id': self.targetid,\n            'attitude': 'heart',\n            'st': self.st,\n        }\n        resp = self.session.post(heartUrl, headers=config.HEADER, data=data)\n        logging.debug('heart create response: %s' % resp.text)\n        return resp.json()\n\n    def successData(self):\n        return {\n            'targetid': self.targetid,\n        }",
    }
  }
}

mixTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "mix",
    "timeout": 3000,
    "params": {
# 默认首先访问 config 结构判断账户
      "uid": uid,
      "st": st,
# 默认首先访问 config 结构判断账户
      "cookies": cookies,
# 默认首先访问 config 结构判断账户
      "tasks": [
        # // 评论
        {
          "taskid": 1,
          "type": "fast_comment",
          "params": {
            "targetmid": 4345461655378681,
            "content": "comment test..."
          }
        },
        # // 转发
        {
          "taskid": 2,
          "type": "fast_repost",
          "params": {
            "targetid": 4345461655378681,
            "targetmid": 4345461655378681,
            "content": "",
            "dualPost": False
          }
        },
        # // 点赞
        {
          "taskid": 3,
          "type": "fast_heart",
          "params": {
            "targetid": 4345461655378681
          }
        },
        # # // 关注
        # {
        #   "type": "friendship",
        #   "params": {
        #     "targetuid": 5846555329,
        #   }
        # },
        # # // 发表
        # {
        #   "type": "update",
        #   "params": {
        #     "content": "update test",
        #   }
        # },
        # {
        #   "type": "pv",
        #   "params": {
        #     "targeturl": "https://weibo.com/6829531006/HbUbUfsch",
        #     "count": 100
        #   }
        # }
      ],
    }
  }
}
# {
#     "taskid": 1543563816,
#     "type": "mix",
#     "err": 0,
#     "data": {
#         "datas": [
#             {
#                 "type": "comment",
#                 "err": 1,
#                 "data": null,
#                 "reason": "blog_not_found"
#             },
#             {
#                 "type": "repost",
#                 "err": 1,
#                 "data": null,
#                 "reason": "blog_not_found"
#             },
#             {
#                 "type": "heart",
#                 "err": 1,
#                 "data": null,
#                 "reason": "blog_not_found"
#             },
#             {
#                 "type": "friendship",
#                 "err": 0,
#                 "data": {
#                     "targetuid": "5846555329"
#                 },
#                 "reason": "done"
#             },
#             {
#                 "type": "update",
#                 "err": 0,
#                 "data": {
#                     "content": "update test"
#                 },
#                 "reason": "done"
#             },
#             {
#                 "type": "pv",
#                 "err": 1,
#                 "data": null,
#                 "reason": "task_not_support"
#             }
#         ]
#     },
#     "reason": "done"
# }

# https://m.weibo.cn/detail/4350173197316243
customizeTask = {
    "code":0,
    "message":"操作成功",
    "data":{
        "taskid":1543563816,
        "type":"customize",
        "timeout":300,
        "params":{
            "datas":[
                {
                    "blockid":"1",
                    "params":{
                        "uid": uid,
                        "st": st,
                        "cookies": cookies,
                        "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
                    },
                    "actions":{
                        # "0":{
                        #     "type":"config_req",
                        #     "params":{

                        #     }
                        # },
                        # "1":{
                        #     "type":"weibo_index_req",
                        #     "params":{
                        #     }
                        # },
                        # "2":{
                        #     "type":"sleep",
                        #     "params":{
                        #         "millisecond":1500
                        #     }
                        # },
                        # "3":{
                        #     "type":"comment_req",
                        #     "params":{
                        #         "targetmid":4341446293054647,
                        #         "content":"后"
                        #     }
                        # },
                        # "4":{
                        #     "type":"repost_req",
                        #     "params":{
                        #         "targetid":4341446293054647,
                        #         "targetmid":4341446293054647,
                        #         "content":"",
                        #         "dualPost":False
                        #     }
                        # },
                        # "5":{
                        #     "type":"heart_req",
                        #     "params":{
                        #         "targetid":4341446293054647
                        #     }
                        # },
                        # "6":{
                        #     "type":"friendship_req",
                        #     "params":{
                        #         "targetuid":5622004557
                        #     }
                        # },
                        "7":{
                            "type":"update_req",
                            "params":{
                                "content": "嘿嘿",
                                "imgurl": "http://127.0.0.1:8888/img.jpg"
                            }
                        }
                    }
                }
            ]
        }
    }
}
hotsearchTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "hotsearch",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,
    }
  }
}
monitorTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "monitor",
    "timeout": 3000,
    "params": {
      # "uid": '1826792401',
      "uid": '5846555329',
      "blog_update_at": '2019-04-01 00:00:00',
    }
  }
}

crawlTask = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "crawl_friends",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,
      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
      "pageno": 2,
    }
  }
}

crawlSecurity = {
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "crawl_security",
    "timeout": 3000,
    "params": {
      "uid": uid,
      "cookies": cookies,
      "st": st,
      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }
  }
}

import time
class Task(tornado.web.RequestHandler):
    def get(self):
        print('fetched task---------------------------------{t}'.format(t=time.time()))
        # self.write(json.dumps(taskPv))
        self.write(json.dumps(loginTask))
        # self.write(json.dumps(heartTask))
        # self.write(json.dumps(fastheartTask))
        # self.write(json.dumps(fastrepostTask))
        # self.write(json.dumps(repostTask))
        # self.write(json.dumps(friendshipTask))
        # self.write(json.dumps(commentTask))
        # self.write(json.dumps(fastCommentTask))
        # self.write(json.dumps(updateTask))
        # self.write(json.dumps(mixTask))
        # self.write(json.dumps(fast_repost))
        # self.write(json.dumps(customizeTask))
        # self.write(json.dumps(crawlTask))

        # self.write(json.dumps(hotsearchTask))
        # self.write(json.dumps(updateEnvTask))
        # self.write(json.dumps(updateBotTask))
        # self.write(json.dumps(monitorTask))
        self.write(json.dumps(crawlSecurity))
        self.finish()

class TaskBack(tornado.web.RequestHandler):
    def post(self):
        data = self.get_argument('data', default=None)
        # with open('result.json', 'a') as f:
        #     f.write(self.request.body.decode('utf-8'))
        print(self.request.body.decode('utf-8'))
        print(time.time())
        self.write(json.dumps({
            'status' : 0
        }))
        self.finish()

a = []
class Test(tornado.web.RequestHandler):
    def get(self):
        a.append(1)
        ip = self.get_argument('ip', default=None)

        print(ip)
        self.write(json.dumps({
            "code": 0,
            "message": "操作成功",
            "data": []
        }))
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/task", Task),
        (r"/taskback", TaskBack),
        (r"/api/v1/task/ip_check", Test),
        (r'/(img\.jpg)', StaticFileHandler, {'path': './'}),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()