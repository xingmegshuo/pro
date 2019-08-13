# coding=utf-8
import time
import re
import logging
import traceback
from tornado import gen, httpclient, ioloop, queues
import config, utils
from utils import tag
from . import BaseBot


now = lambda: int(time.time())

class PvBot(BaseBot):
    name = 'pv'

    def __init__(self, taskid, params):
        super(PvBot, self).__init__(taskid)
        self.readcount = params['count']
        self.targetUrl = params['targeturl']
        self.expires = now() + int(params['timeout'])
        self.badVpnCount = 0
        self.sorryPage = 0
        self.concurrency = config.REQUEST_CONCURRENCY
        self.requestQueue = queues.Queue()
        self.fetching = set()
        self.data = {'count': 0}

    def run(self):
        try:
            io_loop = ioloop.IOLoop.current()
            httpclient.AsyncHTTPClient.configure(config.TORNADO_CLIENT, 
                max_clients=config.MAX_CLIENTS)
            self.client = httpclient.AsyncHTTPClient()
            io_loop.run_sync(self.crawl)
        except Exception as e:
            if e is KeyboardInterrupt:
                self.clearcache()
                raise KeyboardInterrupt
            self.err = 1
            self.reason = config.REASON['bot_run_error']
            self.traceback = traceback.format_exc()
            
    async def crawl(self):
        
        async def worker():
            async for req in self.requestQueue:
                # logging.info(tag('req start', self.taskid))
                if req is None:
                    return
                if not self.err:
                    try:
                        while True:
                            if now() > self.expires:
                                self.err = 1
                                self.reason = config.REASON['timeout']
                                break
                            retry = await self.processReq(req)
                            # logging.info(tag('retry:' + str(retry), self.taskid))
                            # logging.info(tag('badVpnCount: %d, count:%d' % \
                                # (self.badVpnCount, self.data['count']), self.taskid))
                            if (not retry) or self.err:
                                break
                    except Exception as e:
                        logging.error(tag('download error: %s' %
                            traceback.format_exc()))
                self.requestQueue.task_done()

        await self.genBaseReq()
        workers = gen.multi([worker() for _ in range(self.concurrency)])
        await self.requestQueue.join()
        for _ in range(self.concurrency):
            await self.requestQueue.put(None)
        await workers
        if not self.err:
            self.reason = config.REASON['done']

    async def processReq(self, req):
        if req in self.fetching:
            return
        self.fetching.add(req)
        resp = await self.client.fetch(req, raise_error=False)
        retry, count = self.isNetError(resp)
        if retry:
            self.fetching.remove(req)
        
        logging.debug(tag('request {code: %s, qsize: %s count: %s}' % (
            resp.code,
            self.requestQueue.qsize(),
            self.data['count']
        )))
        self.data['count'] += count
        return retry

    async def genBaseReq(self):
        for i in range(self.readcount):
            await self.requestQueue.put(httpclient.HTTPRequest(self.targetUrl,
                headers=config.PV_HEADER, request_timeout=config.REQUEST_TIMEOUT))

    def isNetError(self, resp):
        retry, count = False, 1
        if resp.code == 418 or resp.code == 414:
            count = 0
            self.err = 1
            self.reason = config.REASON['ip_forbidden']
        if resp.code == 599:
            count = 0
            retry = True
            logging.info(tag(config.REASON['bad_vpn'], self.taskid))
            logging.info(tag('resp headers: %s' % resp.headers, self.taskid))
            logging.info(tag('resp : %s' % resp.body, self.taskid))
            self.badVpnCount += 1
        if resp.body:
            if re.findall(br'https://weibo\.com/sorry\?pagenotfound', resp.body):
                self.sorryPage += 1
                retry = True
                count = 0
        else:
            retry = True
            count = 0
        if self.sorryPage > 50:
            retry = False
            self.err = 1
            self.reason = config.REASON['blog_not_found']
        if self.badVpnCount > 50:
            retry = False
            self.reason = config.REASON['bad_vpn']
            self.err = 1
        return retry, count

if __name__ == "__main__":
    params = {
        'count': 10000,
        'targeturl': 'https://weibo.com/1178975384/H7kdmo6q2',
    }
    a = PvBot('123', childPipe(), params)