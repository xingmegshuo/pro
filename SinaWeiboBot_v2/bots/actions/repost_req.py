import logging, json
from . import ActionBase
from config import REASON
from utils import tag

repostUrl = 'https://m.weibo.cn/api/statuses/repost'

class RepostReq(ActionBase):

    name = 'repost_req'

    def crawl(self, targetid, targetmid, content, dualPost):
        code, subcode, url, response, data = 0, None, None, None, {}
        subcode = self.check_blog_not_exist(targetmid)
        if subcode:
            url = 'https://m.weibo.cn/detail/' + str(targetmid)
            code, url, response = 5, url, None
            return code, subcode, url, response, data

        if content == '' or content == 'None' or content is None:
            content = '转发微博'
        dualPost = 1 if dualPost else 0
        reqdata = {
            'id': targetid,
            'content': content if content else '转发微博',
            'dualPost': dualPost,
            'mid': targetmid,
            'st': self.st,
        }
        logging.info(tag('respost_req {data}'.format(data=json.dumps(reqdata))))
        resp = self.session.post(repostUrl, headers=self.headers, data=reqdata)
        logging.info(tag('repost_resp {data}'.format(data=resp.text)))
        respdata = resp.json()

        url, response = repostUrl, respdata
        code, subcode = self.parse_resp(respdata)
        return code, subcode, url, response, data