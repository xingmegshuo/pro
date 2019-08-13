import os
import re
import sys
# from test import create
import config, utils
from daemonize import Daemonize
from taskloop import main as taskloop
# from blogCrawl.blogBot import main as blogcrawl


utils.mkdir(config.CACHE_DIR)

def test():
    # 发表微博
    update()
    # 点赞
    # heart()

def dirname(path):
    return os.path.basename(codefile).split('.')[0]

def daemonize(action, pid, start=True, daemonname='sinaweibobot'):
    daemon = Daemonize(app=daemonname, pid=pid, action=action, chdir='./')
    if start:
        daemon.start()
        return
    daemon.exit()

def cmd():
    command = {
        'test': test,
        'taskloop': taskloop,
        # 'sinasession': sinasession,
        # 'blogCrawl': blogcrawl,
    }
    pid = {
        'taskloop': config.TASK_LOOP_PID,
        # 'sinasession': config.SINA_SESSION_PID,
        # 'blogCrawl': config.BLOG_PID
    }
    argvs = sys.argv
    action, param = None, None
    for i, argv in enumerate(argvs[1:]):
        if i == 0:
            action = argv
        if i == 1:
            param = argv
        if i == 2:
            action, param = None, None
            break
    if action in command:
        if param and param == 'start':
            daemonize(command[action], pid[action], daemonname=action)
            return
        if param and param == 'stop':
            daemonize(command[action], pid[action], start=False, 
                daemonname=action)
            return
        command[action]()

    print('python manager.py %s' % '/'.join([k for k in command.keys()]))


if __name__ == '__main__':
    cmd()
