#coding=utf-8
import base64, time, hashlib, logging, json
import requests
import config
from utils import tag

class Verify(object):

    def __init__(self):
        pass

    def verify(self, img,username):
        return self.verify_feifei(img,username)

    def verify_feifei(self, img,username):
        url = 'http://router.ab.local/cgi-bin/luci/api/ocr'

        files = {
            'img_data':('img_data',img)
        }
        header = {
            'User-Agent': 'Mozilla/5.0',
        }
        resp = requests.post(url, params={'username':username}, files=files ,headers=header)
        logging.info(tag('verify response: %s' % resp.text))
        data = resp.json()
        if data['RetCode'] == 0:
            return data['result']
