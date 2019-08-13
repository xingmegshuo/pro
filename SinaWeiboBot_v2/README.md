## 使用方法

- 环境安装
```
sudo apt-get install -y build-essential
sudo apt-get install -y checkinstall
sudo apt-get install -y libreadline-gplv2-dev
sudo apt-get install -y libncursesw5-dev
sudo apt-get install -y libssl-dev
sudo apt-get install -y libsqlite3-dev
sudo apt-get install -y tk-dev
sudo apt-get install -y libgdbm-dev
sudo apt-get install -y libc6-dev
sudo apt-get install -y libbz2-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y openssl
sudo apt-get install -y libffi-dev
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-setuptools
sudo apt-get install -y libcurl4-openssl-dev
sudo apt-get install -y curl
sudo apt-get install -y wget
wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tar.xz
tar xvf Python-3.7.1.tar.xz
cd Python-3.7.1
./configure --enable-optimizations
sudo make altinstall
pip3.7 install -r requirements.txt
```
- 修改配置文件 ./config.py
  + `config.CODEFILE`  .tar.gz 格式代码压缩包路径
  + `config.HOST_LIST`  批量部署机器 ip 列表
  + `config.PASSWORD`  密码

- 部署\启动\停止
  + 启动爬虫
  `python3.7 manager.py taskloop`
  + 启动爬虫-后台运行
  `python3.7 manager.py taskloop start` or `python3.7 supervisor.py start`
  + 停止后台运行的爬虫
  `python3.7 manager.py taskloop stop`
  + 启动博文爬虫-后台运行
  `python3.7 manager.py blogCrawl start`
  + 批量上传代码
  `python3.7 manager.py putcode`
  + 批量启动爬虫
  `python3.7 manager.py batchstart`
  + 批量停止爬虫
  `python3.7 manager.py batchstop`
  + 批量删除已部署机器上的代码
  `python3.7 manager.py batchrmcode`



### code & subcode

code | subcode | desc | subcode 是否为自定义
----|---- | ---- | ---------
1 | 1001 | 网络错误  | 是
1 | 1002 | ip 已在 30 分钟内使用过 | 是
2 | 2070 | 验证码错误 | 否
2 | 4003 | 账户余额不足，请及时充值 | 否
2 | -1 | 服务器繁忙请稍后重试 | 否
2 | 4004 | 请求失败 | 否
2 | 3010 | 服务器繁忙，请稍候重试或者与客服联系 | 否
3 | 101 | 用户名密码错误 | 否
3 | 20 | 用户不存在 | 否
3 | - | 您已开启登录保护，请扫码登录 | 否
3 | - | 您的帐号尚未激活 | 否
4 | 4001 | 账户被封 | 是
4 | 4002 | 账户被锁 | 是
4 | 4003 | session 过期 | 是
5 | 5001 | 博文不存在 | 是
5 | 20019 | 相同内容请间隔10分钟再进行发布 | 否
5 | 5002 | 点赞操作失败 | 是
5 | 20016 | 发微博太多啦，休息一会儿吧 | 否
5 | 20210 | 作者只允许粉丝评论 | 否
5 | 5003 | 由于作者隐私设置，你没有权限查看此微博 | 是
5 | 5004 | 用户不存在 | 是
5 | - | 根据相关法律法规的要求，此内容无法发布。 | 否
6 | - | 未知异常 | 是



### 自定义任务

#### 配置参数
param | mandatory | description
----|----|------
uid | YES | 账户 uid
st | YES | session st
cookies | YES | session cookies
ua | YES | 登录使用 ua
actions | YES | 操作列表

#### actions 类型及参数

##### weibo_index_req (访问[微博首页](https://m.weibo.cn/)) 无参数

##### sleep (程序暂停)
param | mandatory | description
----|----|------
millisecond | NO | 暂停毫秒数 默认值 1s - 2s

##### comment_req (评论请求)
param | mandatory | description
----|----|------
targetmid | YES | 博文 mid
content | YES | 评论内容

##### repost_req (转发请求)
param | mandatory | description
----|----|------
targetid | YES | 博文 id
targetmid | YES | 博文 mid
dualPost | YES | 是否同时评论原微博
content | YES | 评论内容 没有填 None

##### heart_req (点赞请求)
param | mandatory | description
----|----|------
targetid | YES | 博文 id

##### friendship_req (关注请求)
param | mandatory | description
----|----|------
targetuid | YES | 目标用户 uid

##### update_req (发表请求)
param | mandatory | description
----|----|------
content | 内容或图片必须存在一个或者都存在 | 内容
imgurl | 内容或图片必须存在一个或者都存在 | 图片

```
{
    "code":0,
    "message":"操作成功",
    "data":{
        "taskid":1543563816,
        "type":"customize",
        "timeout":300,
        "params":{
            "datas":[
                {
                    "blockid":"123",
                    "params":{
                        "ua":"..",
                        "uid":"..",
                        "st":"..",
                        "cookies":".."
                    },
                    "actions":{
                        "1":{
                            "type":"read_weibo_index",
                            "params":{

                            }
                        },
                        "2":{
                            "type":"sleep",
                            "params":{
                                "millisecond":1500
                            }
                        },
                        "3":{
                            "type":"comment_req",
                            "params":{
                                "targetmid":4328516705121537,
                                "content":"comment test..."
                            }
                        },
                        "4":{
                            "type":"repost_req",
                            "params":{
                                "targetid":4328516705121537,
                                "targetmid":4328516705121537,
                                "content":"",
                                "dualPost":false
                            }
                        },
                        "5":{
                            "type":"heart_req",
                            "params":{
                                "targetid":4328516705121537
                            }
                        },
                        "6":{
                            "type":"friendship_req",
                            "params":{
                                "targetuid":5622004557
                            }
                        },
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
```

任务返回


```
{
    "taskid": 1543563816,
    "type": "customize",
    "data": {
        "datas": [
            {
                "blockid": "1",
                "params": {
                    "uid": "5846555329"
                },
                "actions": {
                    "1": {
                        "type": "weibo_index_req",
                        "code": 0,
                        "data": {
                            "start_at": 1557910197990,
                            "finished_at": 1557910198020,
                            "uid": "5846555329"
                        },
                        "url": "https://m.weibo.cn/",
                        "taskid": 0
                    },
                    "2": {
                        "type": "sleep",
                        "code": 0,
                        "data": {
                            "start_at": 1557910198021,
                            "finished_at": 1557910199523,
                            "uid": "5846555329"
                        },
                        "taskid": 1
                    },
                    "3": {
                        "type": "comment_req",
                        "code": 0,
                        "data": {
                            "start_at": 1557910199524,
                            "finished_at": 1557910200892,
                            "uid": "5846555329"
                        },
                        "url": "https://m.weibo.cn/api/comments/create",
                        "taskid": 2
                    },
                    "4": {
                        "type": "repost_req",
                        "code": 5,
                        "data": {
                            "start_at": 1557910200894,
                            "finished_at": 1557910201199,
                            "uid": "5846555329"
                        },
                        "subcode": "20016",
                        "url": "https://m.weibo.cn/api/statuses/repost",
                        "response": {
                            "ok": 0,
                            "errno": "20016",
                            "msg": "发微博太多啦，休息一会儿吧!",
                            "error_type": "alert"
                        },
                        "taskid": 3
                    },
                    "5": {
                        "type": "heart_req",
                        "code": 0,
                        "data": {
                            "start_at": 1557910201201,
                            "finished_at": 1557910201609,
                            "uid": "5846555329"
                        },
                        "url": "https://m.weibo.cn/api/attitudes/create",
                        "taskid": 4
                    },
                    "6": {
                        "type": "friendship_req",
                        "code": 0,
                        "data": {
                            "start_at": 1557910201610,
                            "finished_at": 1557910202223,
                            "uid": "5846555329"
                        },
                        "url": "https://m.weibo.cn/api/friendships/create",
                        "taskid": 5
                    }，
                    "7": {
                      "type": "update_req",
                      "code": 0,
                      "data": {
                        "start_at": 1558003755643,
                        "finished_at": 1558003756588,
                        "uid": "5846555329"
                      },
                      "url": "https://m.weibo.cn/api/statuses/update",
                      "taskid": 0
                    }
                }
            }
        ],
        "start_at": 1557910197841,
        "finished_at": 1557910202226
    },
    "code": 0
}
```


### PV 任务
下发任务

param | mandatory | description
----|----|------
targeturl | YES | 目标地址
count | YES | 请求次数

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "timeout": 3000,
    "type": "pv",
    "params": {
      "targeturl": "https://weibo.com/1178975384/Gy43toAH7",
      "count": 10000
    }
  }
}
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "count": 10,
		"finished_at“: "1556865709574",
		”start_at“: "1556865709574"
  },
  "reason": "done"
}
```


### 登录 (炮灰账户登录 type 为 fast_login，等级账户为 normal_login)
下发任务

param | mandatory | description
----|----|------
username | YES | 用户名
password | YES | 密码
checkip | NO | 是否查询当前 ip 并上报

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "normal_login",
    "timeout": 3000,
    "params": {
      "username": "13642572831",
      "password": "dlg30945",
    }
  }
}
```

任务返回示例
```
失败

{
    "taskid": 1543563816,
    "type": "login",
    "data": {
        "username": "18001167287",
        "password": "123123123",
        "start_at": 1557641063301,
        "finished_at": 1557641070900
    },
    "code": 3,
    "subcode": "101",
    "url": "https://login.sina.com.cn/sso/login.php",
    "response": {
        "retcode": "101",
        "reason": "登录名或密码错误"
    }
}
{
    "taskid": 1543563816,
    "type": "login",
    "data": {
        "username": "18001167287",
        "password": "shamao123",
        "start_at": 1557665130108,
        "finished_at": 1557665132258
    },
    "code": 2,
    "subcode": "2070",
    "url": "https://login.sina.com.cn/sso/login.php",
    "response": {
        "retcode": "2070",
        "reason": "输入的验证码不正确"
    }
}

成功
{
    "taskid": 1543563816,
    "type": "login",
    "data": {
        "uid": "5846555329",
        "st": "ca6e65",
        "cookies": "#LWP-Cookies-2.0\nSet-Cookie3: ALF=1560233349; path=\"/\"; domain=\".97973.com\"; path_spec; domain_dot; expires=\"2019-06-11 06:09:09Z\"; version=0\nSet-Cookie3: SSOLoginState=1557641349; path=\"/\"; domain=\".97973.com\"; path_spec; discard; version=0\nSet-Cookie3: ALC=\"ac%3D0%26bt%3D1557641348%26cv%3D5.0%26et%3D1589177348%26ic%3D-562032854%26login_time%3D1557641348%26scf%3D%26uid%3D5846555329%26vf%3D0%26vs%3D0%26vt%3D0%26es%3Da863dc677212dc282d9f06cd3be24272\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; expires=\"2020-05-11 06:09:08Z\"; httponly=None; version=0\nSet-Cookie3: LT=1557641350; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: tgc=\"TGT-NTg0NjU1NTMyOQ==-1557641348-tc-0E56C9D2B0AC7916785D3380BDE47622-1\"; path=\"/\"; domain=\".login.sina.com.cn\"; path_spec; discard; Httponly=None; version=0\nSet-Cookie3: XSRF-TOKEN=ca6e65; path=\"/\"; domain=\".m.weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: SRF=1557641349; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-05-09 06:09:09Z\"; version=0\nSet-Cookie3: SRT=\"D.QqHBJZPtJDYgP!Mb4cYGS4uGiqEMPObOWbBuPEWHNEYd43EJJFMpMERt4EPKRcsrA4kJPOiDTsVuObJnPrybJsydWb9cRZMnSmbs4eW8JsYsW4VpR-4-MePH*B.vAflW-P9Rc0lR-yk!DvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWfIOmp5EYdJ!MPKF9!TsBoW!A-RrEpi49ndDPIJcYPSrnlMc0k4bifVdSONprnSd0lJcM1OFyHMQEJ5mjkOmHII4oCI!HJ5mkCOmzlJ!oCIZHJ5mjlOmHIJ!oCIZHJ5mjlOmHIJ!oCIZHK4qWrWv77\"; path=\"/\"; domain=\".passport.weibo.com\"; path_spec; domain_dot; expires=\"2029-05-09 06:09:09Z\"; httponly=None; version=0\nSet-Cookie3: ALF=1589177348; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:08Z\"; version=0\nSet-Cookie3: SCF=\"Av0sB_0pnZexFjUdib7_S8V2CGSdr6j-pC_l4eesUCgTqUziCvrqqXQ7cBtM1WhN8_8NRmc-Cszfg6IT2K2e6kI.\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2029-05-09 06:09:08Z\"; httponly=None; version=0\nSet-Cookie3: SUB=\"_2A25x08jVDeRhGeNG71QU9SvPyTWIHXVTP-idrDV_PUJbm9AKLWzckW1NS0WOe5HY84PDxnUBjs4EZ5URGAEY1xH5\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:09Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-12xXV2DU8jdkPqvD6cAr5NHD95Qf1hBcSK-fe0z4Ws4DqcjJi--fi-2fi-i2i--Xi-iWi-iWi--4i-2pi-iWi--4i-2pi-iWS0Mt\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: ULOGIN_IMG=\"tc-814ef45bb971fc4dea98bad084d2ae11fbdd\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: sso_info=\"v02m6alo5qztKWRk5SlkJOUpZCkkKWRk5ClkKSEpZCkhKWRk6SlkJOEpZCkhKWRk6SlkJOEpZCkhLeNspm1mpaQvY2ToLSNo5S1jZOMso6QwMA=\"; path=\"/\"; domain=\".sina.com.cn\"; path_spec; domain_dot; expires=\"2020-05-12 06:09:08Z\"; version=0\nSet-Cookie3: ALF=1560233349; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-06-11 06:09:09Z\"; version=0\nSet-Cookie3: MLOGIN=1; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-12 07:09:10Z\"; version=0\nSet-Cookie3: M_WEIBOCN_PARAMS=\"luicode%3D20000174\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-12 06:19:10Z\"; HttpOnly=None; version=0\nSet-Cookie3: SCF=\"Av0sB_0pnZexFjUdib7_S8V2CGSdr6j-pC_l4eesUCgTwJ0hLH5qjq3wEt6VnROi9Xw1jchN8e_RpVrTn32xu3s.\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2029-05-09 06:09:10Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1557641350; path=\"/\"; domain=\".weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: SUB=\"_2A25x08jWDeRhGeNG71QU9SvPyTWIHXVTP-ierDV6PUJbktAKLWv9kW1NS0WOe5xJDz_3NRXc65Lk-Q7zG8l0kp0t\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:10Z\"; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-12xXV2DU8jdkPqvD6cAr5JpX5K-hUgL.Fo-RShqfSK-0eo.2dJLoIEqLxK-LBK-LB.BLxKBLB.2LB.2LxK.LBK2LB.2LxK.LBK2LB.2NS7tt\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:10Z\"; version=0\nSet-Cookie3: SUHB=\"0h15O_-gu01Hsl\"; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:10Z\"; version=0\nSet-Cookie3: WEIBOCN_FROM=1110005030; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: _T_WM=46550733444; path=\"/\"; domain=\".weibo.cn\"; path_spec; domain_dot; expires=\"2019-05-22 06:09:04Z\"; version=0\nSet-Cookie3: ALF=1589177348; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:08Z\"; version=0\nSet-Cookie3: SCF=\"Av0sB_0pnZexFjUdib7_S8V2CGSdr6j-pC_l4eesUCgTqUziCvrqqXQ7cBtM1WhN8xUPBkNgAN4MdBq4Ed2KGpE.\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2029-05-09 06:09:08Z\"; httponly=None; version=0\nSet-Cookie3: SSOLoginState=1557641349; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; version=0\nSet-Cookie3: SUB=_2A25x08jVDeRhGeNG71QU9SvPyTWIHXVSqL0drDV8PUNbmtAKLU3CkW9NS0WOe3_VvZfb4pdIuRwb3XuuG2ce6FuI; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; discard; HttpOnly=None; version=0\nSet-Cookie3: SUBP=\"0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-12xXV2DU8jdkPqvD6cAr5JpX5K2hUgL.Fo-RShqfSK-0eo.2dJLoIEqLxK-LBK-LB.BLxKBLB.2LB.2LxK.LBK2LB.2LxK.LBK2LB.2NS7tt\"; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:09Z\"; version=0\nSet-Cookie3: SUHB=0wnFrVThQyQaGy; path=\"/\"; domain=\".weibo.com\"; path_spec; domain_dot; expires=\"2020-05-11 06:09:09Z\"; version=0\nSet-Cookie3: login=f656a41107fa6197509ed6d05b9390fd; path=\"/\"; domain=\"login.sina.com.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=a902e3917463c16c83238d20c9245191; path=\"/\"; domain=\"passport.97973.com\"; path_spec; discard; version=0\nSet-Cookie3: login=f656a41107fa6197509ed6d05b9390fd; path=\"/\"; domain=\"passport.weibo.cn\"; path_spec; discard; version=0\nSet-Cookie3: login=f656a41107fa6197509ed6d05b9390fd; path=\"/\"; domain=\"passport.weibo.com\"; path_spec; discard; version=0\n",
        "username": "18001167287",
        "password": "shamao123",
        "ua": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36",
        "start_at": 1557641344166,
        "finished_at": 1557641350486
    },
    "code": 0
}
```


### 获取用户首页更新

下发任务

param | mandatory | description
----|----|------
uid | YES | 账户 uid
st | YES | session st
cookies | YES | session cookies
ua | YES | 登录使用 ua
pageno | YES | 抓取页数

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "crawl_friends",
    "timeout": 3000,
    "params": {
      "uid": "..",
      "cookies": "..",
      "st": "..",
      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
      "pageno": 2,
    }
  }
}
```


任务返回示例


```
{
  "taskid": 1543563816,
  "type": "crawl_friends",
  "data": {
    "blogs": [
      {
        "uid": 5622004557,
        "blog_mid": "4372254647048474",
        "created_at": "2019-05-15 16:50:03",
        "summary": "媳妇天天啥事都不干，就知道拍视频   哎"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372251191565437",
        "created_at": "2019-05-15 16:36:19",
        "summary": "既然这么有缘，要不咱们处个对象？  【搞"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372244245811489",
        "created_at": "2019-05-15 16:08:43",
        "summary": "富人的世界我们不懂…… "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372239547826111",
        "created_at": "2019-05-15 15:50:03",
        "summary": "【现场视频！香港的哥怒怼“港独”：香港是"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372235920230242",
        "created_at": "2019-05-15 15:35:38",
        "summary": "哈哈哈哈哈哈哈哈哈哈哈没事  兄弟！<s"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372229116186685",
        "created_at": "2019-05-15 15:08:36",
        "summary": "被放生了<span class=\"url"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372228075979548",
        "created_at": "2019-05-15 15:04:28",
        "summary": "这样拍会不会被打死<span class"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372224447889646",
        "created_at": "2019-05-15 14:50:03",
        "summary": "小姐姐长得这么面善，不像那种做坏事的人，"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372220744558195",
        "created_at": "2019-05-15 14:35:20",
        "summary": "嗯！充实又快乐的一天...<span c"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372217808359562",
        "created_at": "2019-05-15 14:23:40",
        "summary": "厉害了……这要是不拘留就太说不过去了！！"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372214297677806",
        "created_at": "2019-05-15 14:09:43",
        "summary": "女生VS男生，好真实！！   【搞笑】 "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372213865877027",
        "created_at": "2019-05-15 14:08:00",
        "summary": "这算是真正的姐妹了吧 "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372209348435507",
        "created_at": "2019-05-15 13:50:03",
        "summary": "跟别人花同样的钱，比别人享受多倍体验，加"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372205771072762",
        "created_at": "2019-05-15 13:35:50",
        "summary": "我抑郁了<span class=\"url"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372198976427056",
        "created_at": "2019-05-15 13:08:50",
        "summary": "男朋友觉得自己不完整了，该怎么安慰他？ "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372194253364077",
        "created_at": "2019-05-15 12:50:03",
        "summary": "结婚是不可能好好结婚的，就是靠搞笑维持下"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372190562783892",
        "created_at": "2019-05-15 12:35:24",
        "summary": "有一场硬仗要打啊！【搞笑】 "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372179154447749",
        "created_at": "2019-05-15 11:50:03",
        "summary": "抓住布条15分钟顽强等待消防员叔叔救援，"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372178277475400",
        "created_at": "2019-05-15 11:46:35",
        "summary": "哈哈哈哈，编剧有毒，是个魔鬼<span "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372174456860088",
        "created_at": "2019-05-15 11:31:23",
        "summary": "第一批贷款买房的人都怎样了？？？ "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372168609526237",
        "created_at": "2019-05-15 11:08:10",
        "summary": "大逆不道啊！<span class=\"u"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372164050145098",
        "created_at": "2019-05-15 10:50:03",
        "summary": "这就是兄弟，一个眼神一个动作就明白<a "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372153988527382",
        "created_at": "2019-05-15 10:10:04",
        "summary": "你见过最丑的设计是什么？ "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372148950736615",
        "created_at": "2019-05-15 09:50:03",
        "summary": "狗子夜不归宿，主人担心的一夜没睡，天一亮"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372145389733422",
        "created_at": "2019-05-15 09:35:53",
        "summary": "大哥耿直，喝阔乐<span class="
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372138355610427",
        "created_at": "2019-05-15 09:07:57",
        "summary": "打…屁屁？<span class=\"ur"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372133851884177",
        "created_at": "2019-05-15 08:50:03",
        "summary": "考拉妈妈太有爱了，母爱不分物种<span"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372132479751305",
        "created_at": "2019-05-15 08:44:35",
        "summary": "<a  href=\"https://m."
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372132114815423",
        "created_at": "2019-05-15 08:43:09",
        "summary": "<a  href=\"https://m."
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372123633836372",
        "created_at": "2019-05-15 08:09:27",
        "summary": "不能丢失了五千年的传统文化 <span "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372118751748638",
        "created_at": "2019-05-15 07:50:03",
        "summary": "还记得罗永浩怼星巴克服务员的视频吗？看一"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372115283717112",
        "created_at": "2019-05-15 07:36:16",
        "summary": "兄弟你真自私，我也想有参与感。 【搞笑】"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372107967887311",
        "created_at": "2019-05-15 07:07:12",
        "summary": "你不曾遇到的尴尬<span class="
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372103652272827",
        "created_at": "2019-05-15 06:50:03",
        "summary": "谁能告诉我，要怎样才能拥有这样的女人？<"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372099944505028",
        "created_at": "2019-05-15 06:35:19",
        "summary": "睡前小故事<span class=\"ur"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372069745496929",
        "created_at": "2019-05-15 04:35:19",
        "summary": "6得一匹 "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372062221606516",
        "created_at": "2019-05-15 04:05:25",
        "summary": "小小年纪出了三次名！真是厉害了小哥哈哈哈"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372054671060492",
        "created_at": "2019-05-15 03:35:25",
        "summary": "再穷不能穷孩子，看得我都泪目了。。。【搞"
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372047348003834",
        "created_at": "2019-05-15 03:06:19",
        "summary": "告诉我，哪个是错的? "
      },
      {
        "uid": 5622004557,
        "blog_mid": "4372039559242320",
        "created_at": "2019-05-15 02:35:22",
        "summary": "女人嫉妒心真了不起<span class"
      }
    ],
    "start_at": 1557910469344,
    "finished_at": 1557910470234
  },
  "code": 0
}
```




### 获取用户安全中心信息

下发任务

param | mandatory | description
----|----|------
uid | YES | 账户 uid
st | YES | session st
cookies | YES | session cookies
ua | YES | 登录使用 ua

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "crawl_security",
    "timeout": 3000,
    "params": {
      "uid": "..",
      "cookies": "..",
      "st": "..",
      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }
  }
}
```

任务返回示例


```
{
  "taskid": 1543563816,
  "type": "crawl_security",
  "data": {
    "msgs": [
      {
        "text": "<a data-url=\"http://t.cn/EKn3rm3\" href=\"http://t.cn/EKn3rRz?wbtpuuid=1e566d412a8e0c3758bc3942cf34abcd2695\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web_default.png'></span><span class=\"surl-text\">登录提醒</span></a>",
        "id": "4373020074693886",
        "created_at": "2019-05-17 19:31:35"
      },
      {
        "text": "<a data-url=\"http://t.cn/EKHdvS2\" href=\"https://security.weibo.com/loginrecord/active?showmenu=0&cfrom=new&wbtpuuid=2a036aa8099a933c27dd5cc1498c08a53105\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web_default.png'></span><span class=\"surl-text\">帐号与安全提醒</span></a>",
        "id": "4372854022258651",
        "created_at": "2019-05-17 08:31:45"
      },
      {
        "text": "你已成功修改密码！请牢记你的帐号密码，点击<a href='http://t.cn/R3ZBo1X' data-hide=''><span class='url-icon'><img style='width: 1rem;height: 1rem' src='//h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web_default.png'></span> <span class='surl-text'>网页链接</span></a>查看更多安全设置。",
        "id": "4354278707536967",
        "created_at": "2019-03-27 02:20:05"
      }
    ],
    "start_at": 1558093832839,
    "finished_at": 1558093843169
  },
  "code": 0
}
```







































reason | description
----|----
done | 成功
ip_forbidden | ip 封禁
bad_vpn | 599 代理服务器连接超时
bot_run_error | 爬虫运行异常
bad_account | 用户名密码错误
account_expired | 账户登录 session 过期
timeout | 任务执行超时
blog_not_found | 目标博文不存在
account_forbidden | 帐号处于锁定状态
account_not_found | 目标账户不存在
task_not_support | 不支持的任务
comment_repeat | 相同内容发布未间隔10分钟（评论、转发并评论、发表）
frequent_login | 当前线路 ip 30分钟内已进行了一次登录
heart_operate_fail | 点赞任务返回 操作失败
frequent_comment | 评论操作频繁
frequent_repost | 转发操作频繁
only_allows_fans_comment | 作者只允许粉丝评论
account_forbidden_originally | 首次登录被封禁
net_err | 网络错误
no_permission | 由于作者隐私设置，没有权限操作此微博
censor_forbidden | 根据相关法律法规的要求，此内容无法发布。

### 点赞
下发任务

param | mandatory | description
----|----|------
targetid | YES | 目标博文 id
st | YES | 用户认证 st
uid | YES | 用户 uid
cookies | YES | 用户认证 cookies

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "heart",
    "timeout": 3000,
    "params": {
      "targetid": 4313239095972249,
      "st": "6fefe5",
      "uid": "6829531006",
      "cookies": ".....",
    }
  }
}
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "targetid": "4313239095972249"
  },
  "reason": "done"
}
```


### 转发
下发任务

param | mandatory | description
----|----|------
uid | YES | 用户 uid
cookies | YES | 用户认证 cookies
st | YES | 用户认证 st
targetid | YES | 目标博文 id
targetmid | YES | 目标博文 mid
content | NO | 评论
dualPost | YES | 是否同时评论原博文

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "repost",
    "timeout": 3000,
    "params": {
      "uid": "6829531006",
      "cookies": "........",
      "st": "6fefe5",
      "targetid": 4313239095972249,
      "targetmid": 4313239095972249,
      "content": "",
      "dualPost": false,
    }
  }
}
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "targetid": "4313239095972249",
    "targetmid": "4313239095972249",
    "content": "转发微博",
    "dualPost": 0
  },
  "reason": "done"
}
```

### 关注
下发任务

param | mandatory | description
----|----|------
uid | YES | 用户 uid
cookies | YES | 用户认证 cookies
st | YES | 用户认证 st
targetuid | YES | 目标用户 id

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "friendship",
    "timeout": 3000,
    "params": {
      "uid": "6829531006",
      "cookies": "......",
      "st": "6fefe5",
      "targetuid": 5846555329,
    }
  }
}
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "targetuid": "5846555329"
  },
  "reason": "done"
}
```

### 评论
下发任务

param | mandatory | description
----|----|------
uid | YES | 用户 uid
cookies | YES | 用户认证 cookies
st | YES | 用户认证 st
targetmid | YES | 目标博文 mid
content | YES | 评论内容

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "comment",
    "timeout": 3000,
    "params": {
      "uid": "6829531006",
      "cookies": ".....",
      "st": "6fefe5",
      "targetmid": 4313239095972249,
      "content": "comment test",
    }
  }
}
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "content": "comment test",
    "targetmid": "4313239095972249"
  },
  "reason": "done"
}
```

### 发表
下发任务

param | mandatory | description
----|----|------
uid | YES | 用户 uid
cookies | YES | 用户认证 cookies
st | YES | 用户认证 st
content | YES | 博文内容

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "update",
    "timeout": 3000,
    "params": {
      "uid": "6829531006",
      "cookies": "......",
      "st": "6fefe5",
      "content": "update test",
    }
  }
}
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "content": "update test"
  },
  "reason": "done"
}
```

### 混合任务
1. 支持任务：点赞、评论、转发、发表、关注（需要登录的任务）
1. 任务列表不限个数，类型可重复；任务连续执行，应尽量少的分配执行任务
1. 任务返回是单个任务的返回去掉 taskid 字段，添加一个 type 字段，其他完全一致
1. 爬虫返回注意：
  - 外层 reason 只会返回 done 或者 bot_run_error，bot_run_error 代表了整个混合任务的失败
  - 调度应以内层 reason 为每个任务的实际 reason

param | mandatory | description
----|----|------
tasks | YES | 任务列表，具体参数见下例

```
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "taskid": 1543563816,
    "type": "mix",
    "timeout": 3000,
    "params": {
      "uid": "6829531006",
      "st": "6fefe5",
      "cookies": "......",
      "tasks": [
        // 评论
        {
          "type": "comment",
          "params": {
            "targetmid": 4313239095972249,
            "content": "comment test"
          }
        },
        // 转发
        {
          "type": "repost",
          "params": {
            "targetid": 4313239095972249,
            "targetmid": 4313239095972249,
            "content": "",
            "dualPost": false
          }
        },
        // 点赞
        {
          "type": "heart",
          "params": {
            "targetid": 4313239095972249
          }
        },
        // 关注
        {
          "type": "friendship",
          "params": {
            "targetuid": 5846555329,
          }
        },
        // 发表
        {
          "type": "update",
          "params": {
            "content": "update test",
          }
        }
      ],
    }
  }
}
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "datas": [
      // 任务返回是单个任务的返回去掉 taskid 字段，添加一个 type 字段，其他完全一致
      {
        "type": "comment",
        "err": 1,
        "data": null,
        "reason": "content_repeat"
      },
      {
        "type": "repost",
        "err": 0,
        "data": {
          "targetid": "4328516705121537",
          "targetmid": "4328516705121537",
          "content": "转发微博",
          "dualPost": 0
        },
        "reason": "done"
      },
      {
        "type": "heart",
        "err": 0,
        "data": {
          "targetid": "4328516705121537"
        },
        "reason": "done"
      },
      {
        "type": "friendship",
        "err": 0,
        "data": {
          "targetuid": "5846555329"
        },
        "reason": "done"
      },
      {
        "type": "update",
        "err": 0,
        "data": {
          "content": "update test"
        },
        "reason": "done"
      },
      // 如果你匹配了不支持的任务
      {
        "type": "pv",
        "err": 1,
        "data": null,
        "reason": "task_not_support"
      }
    ]
  },
  "reason": "done"
}
```




### 更新爬虫脚本
下发任务

param | mandatory | description
----|----|------
bot | YES | 脚本文件名，如不存在将会创建新脚本，若存在将脚本内容更新为 content
content | YES | 更新内容

```
{
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
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "bot": "testBot.py",
    "content": "#coding=utf-8\nimport logging\nimport sinaRequests as requests\nimport config\nfrom . import CreateBaseBot\n\n\nheartUrl = 'https://m.weibo.cn/api/attitudes/create'\n\nclass HeartBot(CreateBaseBot):\n\n    name = 'test'\n    \n    def __init__(self, taskid, childPipe, params):\n        cookies = params['cookies']\n        uid = str(params['uid'])\n        self.st = params['st']\n        super(HeartBot, self).__init__(taskid, childPipe, uid, cookies)\n        self.targetid = str(params['targetid'])\n\n    def createReq(self):\n        data = {\n            'id': self.targetid,\n            'attitude': 'heart',\n            'st': self.st,\n        }\n        resp = self.session.post(heartUrl, headers=config.HEADER, data=data)\n        logging.debug('heart create response: %s' % resp.text)\n        return resp.json()\n\n    def successData(self):\n        return {\n            'targetid': self.targetid,\n        }"
  },
  "reason": "done"
}
```

### 更新环境
下发任务

param | mandatory | description
----|----|------
sh | YES | 需要运行的脚本内容

```
{
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
```
任务返回
```
{
  "taskid": 1543563816,
  "err": 0,
  "data": {
    "stdout": "/home/lai/project_py/SinaWeiboBot\n总用量 166\ndrwxrwxrwx 1 root root  4096 12月  4 15:48 .\ndrwxrwxrwx 1 root root  4096 11月 30 15:30 ..\n-rwxrwxrwx 1 root root  1488 12月  1 16:23 api.py\n-rwxrwxrwx 1 root root  1939 12月  3 18:17 api.pyc\ndrwxrwxrwx 1 root root  4096 12月  4 17:00 bots\ndrwxrwxrwx 1 root root   160 12月  4 17:42 Cache\n-rwxrwxrwx 1 root root  2244 12月  2 14:30 config.py\n-rwxrwxrwx 1 root root  1682 12月  3 18:17 config.pyc\n-rwxrwxrwx 1 root root  3685 12月  2 13:53 cookies.txt\ndrwxrwxrwx 1 root root     0 11月 30 10:51 docs\ndrwxrwxrwx 1 root root  4096 12月  4 17:45 .git\n-rwxrwxrwx 1 root root    55 11月 30 15:16 .gitignore\n-rwxrwxrwx 1 root root     0 11月 30 10:23 __init__.py\n-rwxrwxrwx 1 root root  1106 11月 30 10:45 install_python\n-rwxrwxrwx 1 root root   534 11月 30 16:37 log.py\ndrwxrwxrwx 1 root root  4096 12月  2 14:39 __pycache__\n-rwxrwxrwx 1 root root 10340 12月  4 17:28 query.py\n-rwxrwxrwx 1 root root 15986 12月  4 16:58 README.md\n-rwxrwxrwx 1 root root   147 11月 30 10:44 requirements.txt\n-rwxrwxrwx 1 root root 73229 12月  4 17:47 result.json\n-rwxrwxrwx 1 root root  4260 12月  4 17:00 supervisor.py\n-rwxrwxrwx 1 root root  1633 12月  2 14:48 test.html\n-rwxrwxrwx 1 root root  3269 12月  4 15:47 test.py\n-rwxrwxrwx 1 root root  1585 12月  2 14:34 utils.py\ndrwxrwxrwx 1 root root     0 12月  2 14:03 .vscode\n",
    "stderr": ""
  },
  "reason": "done"
}
```
