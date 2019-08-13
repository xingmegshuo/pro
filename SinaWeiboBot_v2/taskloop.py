# coding=utf-8
import sys
import time
import json
import copy
import logging
import inspect
import traceback

from requests.exceptions import ReadTimeout
import sinaRequests as requests
from bots import BaseBot, CreateBaseBot
import config, utils
from utils import tag

class Taskloop(object):
    #初始化开始任务
    def runWorker(self, task):
        taskid, type, params, timeout = (task['taskid'], task['type'],
            task['params'], task['timeout'])
        params_copy = copy.deepcopy(params)
        if 'cookies' in params_copy:
            params_copy['cookies'] = '..'
        logging.info(tag('fetch task: %s|%s|%s' % (taskid, type, params_copy)))
        # 原来 timeout 是在 taskloop 以创建进程的方式监控
        # 现在针对 pv 任务，在内部循环中处理超时，去除其他任务的超时处理（其他任务无需请求大量链接做耗时处理）
        # 将 timeout 参数加入 params 中，传入爬虫
        params['timeout'] = timeout
        worker = self.taskWorkers[type](taskid, params)
        time.sleep(config.START_TASK_DELAY)
        worker.run()
        return worker

    def fetchTask(self):
        #获取任务
        task_service = [
            (config.FAST_TASK_URL, config.FAST_TASK_BACK_URL),
            (config.TASK_URL, config.TASK_BACK_URL),
        ]
        for fetchurl, reporturl in task_service:
            try:
                resp = requests.get(fetchurl)
                logging.info(tag('fetch url %s resp: %s' % (
                    fetchurl, resp.text)))
                task = resp.json()
            except:
                logging.error(tag('fetch url %s error: %s' % (
                    fetchurl, traceback.format_exc())))
                continue
            if 'data' in task:
                if task['data']:
                    return task['data'], reporturl
            if 'code' in task:
                if task['code'] == 40007:
                    logging.info(tag('resp code 40007 not have fast task'))
        return None, None


    def run(self):
        while True:
            # 每次任务开始之前重载爬虫，因为下发任务中可能包含更新爬虫脚本
            self.taskWorkers = getBotsFromModule('bots')
            try:
                task, report_url = self.fetchTask()
            except:
                task = None
                logging.error(tag('Taskloop fetch task error: %s' % traceback.format_exc()))
            if task is None:
                logging.info(tag('not task'))
                time.sleep(config.FETCH_TASK_DELAY())
                continue
            try:
                worker = self.runWorker(task)
            except Exception as e:
                worker = None
                if e is KeyboardInterrupt:
                    raise KeyboardInterrupt
                logging.error(tag('Taskloop run error: %s' % traceback.format_exc()))
            if worker is None:
                continue
            showWorkerResult(worker)
            try:
                self.report(worker, report_url)
            except:
                logging.error(tag('Report error: %s' % traceback.format_exc()))

    def report(self, worker, report_url):
        headers = { 
            "Content-Type":"application/json" 
        }

        result = {
            'taskid': worker.taskid,
            'type': worker.name,
            'data': worker.data,
        }
        result['code'] = worker.code
        if worker.code != 0:
            if worker.subcode:
                result['subcode'] = worker.subcode
            if worker.url:
                result['url'] = worker.url
            if worker.response:
                result['response'] = worker.response
            
        logging.info(tag('task back req: %s' % json.dumps(result)))
        count = config.REPORT_RETRY
        while count:
            try:
                resp = requests.post(report_url, headers=headers, 
                    json=result)
            except Exception as e:
                if e is TimeoutError:
                    count -= 1
                    continue
                raise e
            else:
                break
        logging.info(tag('task back resp: %s' % resp.text))
        return resp

def showWorkerResult(worker):
    result = {
        'code': worker.code,
        'subcode': worker.subcode,
        'url': worker.url,
        'response': worker.response,

        'taskid': worker.taskid,
        'type': worker.name,
        'data': worker.data,
        'traceback': worker.traceback
    }
    logging.info(tag('worker result:'))
    for title, info in result.items():
        logging.info(tag('      %s:%s' % (title, info)))

def iterBotClasses(module_name):
    for module in utils.walk_modules(module_name):
        for obj in vars(module).values():
            if inspect.isclass(obj) and issubclass(obj, BaseBot) and \
                    obj.__module__ == module.__name__ and \
                    not obj == BaseBot and \
                    not obj == CreateBaseBot:
                yield obj

def getBotsFromModule(module):
    b = {}
    for bot in iterBotClasses(module):
        b[bot.name] = bot
    logging.debug(tag('load task worker %s' % b))
    return b

def main():
    # utils.initlog(config.LOG_LEVEL, filename=config.LOG_FILE, sendSyslog=True)
    #utils.initlog(config.LOG_LEVEL, filename=None, sendSyslog=True)
    utils.mkdir(config.CACHE_DIR)
    Taskloop().run()

if __name__ == '__main__':
    main()