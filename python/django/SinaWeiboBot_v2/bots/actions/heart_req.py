import logging, json
from . import ActionBase
from config import REASON
import sinaRequests as requests
from utils import tag

heartUrl = 'https://m.weibo.cn/api/attitudes/create'

class HeartReq(ActionBase):

    name = 'heart_req'

    def crawl(self, targetid):
        code, subcode, url, response, data = 0, None, None, None, {}
        subcode = self.check_blog_not_exist(targetid)
        if subcode:
            url = 'https://m.weibo.cn/detail/' + str(targetid)
            code, url, response = 5, url, None
            return code, subcode, url, response, data

        reqdata = {
            'id': targetid,
            'attitude': 'heart',
            'st': self.st,
        }
        logging.info(tag('heart_req {data}'.format(data=json.dumps(reqdata))))
        resp = self.session.post(heartUrl, headers=self.headers, data=reqdata)
        logging.info(tag('heart_resp {data}'.format(data=resp.text)))
        respdata = resp.json()

        url, response = heartUrl, respdata
        code, subcode = self.parse_resp(respdata)
        return code, subcode, url, response, data