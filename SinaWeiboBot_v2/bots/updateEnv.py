#coding=utf-8
import os
import logging
import traceback
import shlex
from subprocess import Popen, PIPE
import config, utils
from utils import tag

from . import BaseBot

class UpdateEnv(BaseBot):

    name = 'updateEnv'
    
    def __init__(self, taskid, params):
        super(UpdateEnv, self).__init__(taskid)
        self.sh = params['sh']

    def crawl(self):
        shname = os.path.join(config.CACHE_DIR, str(self.taskid) + '.sh')
        self.cachefiles.append(shname)
        shOutName = os.path.join(config.CACHE_DIR, str(self.taskid) + '.out')
        self.cachefiles.append(shOutName)
        with open(shname, 'w') as f:
            f.write(self.sh)
        command_line = 'sh %s' % shname
        args = shlex.split(command_line)
        process = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        logging.debug(tag('stdout: %s' % stdout))
        logging.debug(tag('stderr: %s' % stderr))
        self.reason = config.REASON['done']
        self.data = {
            'stdout': stdout.decode('utf-8'),
            'stderr': stderr.decode('utf-8'),
        }