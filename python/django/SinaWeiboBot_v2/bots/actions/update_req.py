import logging, json
from . import ActionBase
from config import REASON
import sinaRequests as requests
from utils import tag
import config

updateUrl = 'https://m.weibo.cn/api/statuses/update'
uploadPicUrl = 'https://m.weibo.cn/api/statuses/uploadPic'

class UpdateReq(ActionBase):

    name = 'update_req'

    def crawl(self, content=None, imgurl=None):
        if imgurl is None:
            return self.update(content)
        return self.update_pic(imgurl, content)

    def update(self, content):
        code, subcode, url, response, data = 0, None, None, None, {}
        reqdata = {
            'content': content,
            'st': self.st,
        }
        logging.info(tag('update_req {data}'.format(data=json.dumps(reqdata))))
        resp = self.session.post(updateUrl, headers=self.headers, data=reqdata)
        logging.info(tag('update_resp {data}'.format(data=resp.text)))
        respdata = resp.json()

        url, response = updateUrl, respdata
        code, subcode = self.parse_resp(respdata)
        return code, subcode, url, response, data

    def update_pic(self, imgurl, content=None):
        code, subcode, url, response, data = 0, None, None, None, {}
        if content is None or content == '':
            content = '分享图片'
        imgfile, name, imgtype = self.getimg(imgurl)
        logging.info(tag('img {name} {imgtype}'.format(name=name, imgtype=imgtype)))
        reqdata = {
            'type': 'json',
            'st': self.st,
        }
        reqdata={
            'type': (None, 'json'),
            'st': (None, self.st),
            'pic':(name, open(imgfile, 'rb'), imgtype),
        }
        headers = {
            'authority': 'm.weibo.cn',
            'method': 'POST',
            'path': '/api/statuses/uploadPic',
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'origin': 'https://m.weibo.cn',
            'referer': 'https://m.weibo.cn/compose/',
            'user-agent': self.ua,
            'x-requested-with': 'XMLHttpRequest',
        }
        resp = self.session.post(uploadPicUrl, headers=headers, files=reqdata)
        logging.info(tag('uploadPicUrl_resp {data}'.format(data=resp.text)))
        if not ('pic_id' in resp.json()):
            code = 5
            return code, subcode, uploadPicUrl, resp.json(), data
        pic_id = resp.json()['pic_id']
        reqdata = {
            'content': content,
            'st': self.st,
            'picId': pic_id
        }
        logging.info(tag('update_req {data}'.format(data=json.dumps(reqdata))))
        resp = self.session.post(updateUrl, headers=self.headers, data=reqdata)
        logging.info(tag('update_resp {data}'.format(data=resp.text)))
        respdata = resp.json()
        url, response = updateUrl, respdata
        code, subcode = self.parse_resp(respdata)
        return code, subcode, url, response, data

    def getimg(self, url):
        resp = requests.get(url)
        name = url.split('/')[-1]
        imgfile = config.CACHE_DIR + '/' + name
        with open(imgfile, 'wb') as f:
            f.write(resp.content)
        self.cachefiles.append(imgfile)
        imgtype = name.split('.')[-1]
        if imgtype == 'jpg':
            imgtype = 'jpeg'
        imgtype = 'image/' + imgtype
        return imgfile, name, imgtype
