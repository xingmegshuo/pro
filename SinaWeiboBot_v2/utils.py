import os
import re
import sys
import base64
import logging, time
from logging.handlers import SysLogHandler
from datetime import datetime, timedelta
from importlib import import_module
from pkgutil import iter_modules



projectDir = os.path.dirname(os.path.realpath(__name__))
timestamp = lambda: int(time.time() * 1000) 

def walk_modules(path):
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods

def strftime(t):
    return t, t.strftime('%Y-%m-%d %H:%M:%S')

def formatDate(s):
    if re.match(r"刚刚", s):
        return datetime.now()
    m = re.match(r"(\d+)分钟前", s)
    if m:
        m = m.groups()[0]
        return datetime.now() - timedelta(minutes=int(m))
    
    h = re.match(r"(\d+)小时前", s)
    if h:
        h = h.groups()[0]
        return datetime.now() - timedelta(hours=int(h))
    t = re.match(r"昨天( [0-9:]+)", s)
    if t:
        s = t.groups()[0]
        s = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + s + ':00'
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    if re.match(r"\d{2}-\d{2}", s):
        s = str(datetime.now().year) + '-' + s + ' 00:00:00'
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    if re.match(r"\d{4}-\d{2}-\d{2}", s):
        s += ' 00:00:00'
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def mkdir(d):
    if not os.path.exists(d):
        os.mkdir(d)

def tag(s, taskid=None):
    if taskid:
        s = str(taskid) + ':' + s
    return 'spider ' + s

def initlog(level, filename=None, sendSyslog=True):
    logging.basicConfig(level=level,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=filename,
        filemode='a'
    )
    logger = logging.getLogger()
    # logger.addHandler(logging.StreamHandler())
    if sendSyslog:
        syslogHander = logging.handlers.SysLogHandler(address='/dev/log')
        logger.addHandler(syslogHander)

if __name__ == '__main__':
    # print(formatDate('刚刚'))
    # print(formatDate('5分钟前'))
    # print(formatDate('1小时前'))
    # print(formatDate('昨天 11:15'))
    # print(formatDate('11-18'))
    # print(formatDate('2017-03-24'))
    print(projectDir)
    print(walk_modules(projectDir))
