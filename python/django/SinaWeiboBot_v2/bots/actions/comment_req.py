import logging, json
from . import ActionBase
from config import REASON
from utils import tag

commentUrl = 'https://m.weibo.cn/api/comments/create'

class CommentReq(ActionBase):

    name = 'comment_req'

    def crawl(self, targetmid, content):
        code, subcode, url, response, data = 0, None, None, None, {}
        subcode = self.check_blog_not_exist(targetmid)
        if subcode:
            url = 'https://m.weibo.cn/detail/' + str(targetmid)
            code, url, response = 5, url, None
            return code, subcode, url, response, data

        reqdata = {
            'content': content,
            'mid': targetmid,
            'st': self.st,
        }
        logging.info(tag('comment_req {data}'.format(data=json.dumps(reqdata))))
        resp = self.session.post(commentUrl, headers=self.headers, data=reqdata)
        logging.info(tag('comment_resp {data}'.format(data=resp.text)))
        respdata = resp.json()

        url, response = commentUrl, respdata
        code, subcode = self.parse_resp(respdata)
        return code, subcode, url, response, data
