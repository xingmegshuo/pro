import logging
from . import ActionBase
from config import REASON
from utils import tag


class WeiboIndexReq(ActionBase):

    name = 'weibo_index_req'

    def crawl(self):
        logging.info(tag('weibo_index_req'))
        code, subcode, url, response, data = 0, None, None, None, {}
        url = 'https://m.weibo.cn/'
        resp = self.session.get(url, headers=self.headers)
        return code, subcode, url, response, data