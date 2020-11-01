#coding=utf-8
import logging, json, time, random, os, traceback
import http.cookiejar as cookielib
from requests.exceptions import ConnectionError as requests_ConnectionError
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout 
import sinaRequests as requests
import config
from . import BaseBot
from bots.commentBot import CommentBot, FastCommentBot
from bots.heartBot import HeartBot, FastHeartBot
from bots.repostBot import RepostBot, FastRepostBot
from bots.updateBot import UpdateBot
from bots.friendshipBot import FriendshipBot
from utils import tag



workers = {
    CommentBot.name : CommentBot,
    HeartBot.name : HeartBot,
    RepostBot.name : RepostBot,
    UpdateBot.name : UpdateBot,
    FriendshipBot.name : FriendshipBot,
    FastCommentBot.name : FastCommentBot,
    FastHeartBot.name : FastHeartBot,
    FastRepostBot.name : FastRepostBot,
}

class MixBot(BaseBot):

    name = 'mix'

    def __init__(self, taskid, params):
        self.cookies = params['cookies']
        self.uid = str(params['uid'])
        self.st = params['st']
        self.tasks = params['tasks']
        self.session = self.initSession(self.uid, self.cookies)
        super(MixBot, self).__init__(taskid)
        self.data = {
            'datas': []
        }

    def initSession(self, uid, cookies):
        session = requests.session()
        cookiefile = config.CACHE_DIR + '/' + uid + '.cookies'
        with open(cookiefile, 'w') as f:
            f.write(cookies)
        # self.cachefiles.append(cookiefile)
        session.cookies = cookielib.LWPCookieJar()
        session.cookies.load(filename=cookiefile)
        logging.info(tag('init session uid: %s' % uid))
        os.remove(cookiefile)
        return session

    def run(self):
        try:
            self.crawl()
        except Exception as e:
            if e is KeyboardInterrupt:
                self.clearcache()
                raise KeyboardInterrupt
            if isinstance(e, requests_ConnectionError) or isinstance(e, ConnectTimeout) or isinstance(e, ReadTimeout):
                self.gen_run_err(config.REASON['net_err'])
                self.err = 1
                self.reason = config.REASON['net_err']
                self.traceback = traceback.format_exc()
            else:
                self.gen_run_err(config.REASON['bot_run_error'])
                self.err = 1
                self.reason = config.REASON['bot_run_error']
                self.traceback = traceback.format_exc()
        self.clearcache()

    def gen_run_err(self, reason):
        for task in self.tasks:
            taskid = task['taskid']
            type = task['type']
            result = {
                'taskid': taskid,
                'type': type,
                'err': 1,
                'data': None,
                'reason': reason,
            }
            self.data['datas'].append(result)

    def crawl(self):
        config_req(session=self.session)
        weibo_index_req(session=self.session)
        for task in self.tasks:
            params = task['params']
            type = task['type']
            params['cookies'] = self.cookies
            params['uid'] = self.uid
            params['st'] = self.st
            worker = workers.get(type, None)
            logging.info(tag('mix sub task start: %s' % worker))
            if worker is None:
                logging.error(tag('task_not_support: %s' % type))
                self.data['datas'].append({
                    'type': type,
                    'err': 1,
                    'data': None,
                    'reason': config.REASON['task_not_support']
                })
                continue
            taskid = task['taskid']
            worker = worker(taskid, params)
            worker.run()
            result = {
                'taskid': worker.taskid,
                'type': worker.name,
                'err': worker.err,
                'data': worker.data,
                'reason': worker.reason,
                'traceback': worker.traceback
            }
            logging.info(tag('mix sub task: %s worker result:' % worker))
            for title, info in result.items():
                logging.info(tag('      %s:%s' % (title, info)))
            del result['traceback']
            # del result['taskid']
            self.data['datas'].append(result)
            time.sleep(random.uniform(1, 2))
        self.reason = config.REASON['done']

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
