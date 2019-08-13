import logging, json
from . import ActionBase
from config import REASON
from utils import tag

friendshipUrl = 'https://m.weibo.cn/api/friendships/create'

class FriendshipReq(ActionBase):

    name = 'friendship_req'

    def crawl(self, targetuid):
        code, subcode, url, response, data = 0, None, None, None, {}
        subcode = self.check_user(targetuid)
        if subcode:
            url = 'https://m.weibo.cn/profile/info'
            code, url, response = 5, url, None
            return code, subcode, url, response, data

        reqdata = {
            'uid': targetuid,
            'st': self.st,
        }
        logging.info(tag('friendship_req {data}'.format(data=json.dumps(reqdata))))
        resp = self.session.post(friendshipUrl, headers=self.headers, data=reqdata)
        logging.info(tag('friendship_resp {data}'.format(data=resp.text)))
        respdata = resp.json()

        url, response = friendshipUrl, respdata
        code, subcode = self.parse_resp(respdata)
        return code, subcode, url, response, data