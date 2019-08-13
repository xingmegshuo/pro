#coding=utf-8
import datetime
import os
import re
import json
import time
import random
import sinaRequests as requests
import logging
import traceback
import config, utils
from utils import tag

from . import BaseBot


class UpdateSelf(BaseBot):

    name = 'updateBot'
    
    def __init__(self, taskid, params):
        super(UpdateSelf, self).__init__(taskid)
        self.bot = params['bot']
        self.content = params['content']

    def crawl(self):
        pwd = os.path.split(os.path.abspath(__file__))[0]
        fn = os.path.join(pwd, self.bot)
        with open(fn, 'w') as f:
            f.write(self.content)
        self.reason = config.REASON['done']
        self.data = {
            'bot':self.bot,
            'content': self.content
        }