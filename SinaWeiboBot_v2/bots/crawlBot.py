#coding=utf-8
import logging, time, random, re
from datetime import datetime, timedelta
import sinaRequests as requests
import config
from . import BaseBot
from utils import tag

#抓取更新的微博文章
class CrawlBot(BaseBot):

    name = 'monitor'

    def __init__(self, taskid, params):
        self.uid = str(params['uid'])
        blog_update_at = params['blog_update_at']
        if not (blog_update_at == 'None' or blog_update_at is None):
            self.blog_update_at = datetime.strptime(blog_update_at, 
                "%Y-%m-%d %H:%M:%S")
        else:
            self.blog_update_at = None
        super(CrawlBot, self).__init__(taskid)

    def crawl(self):
        update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        resp = get_userinfo(self.uid)
        data = resp.json()['data']
        account_id = data['user']['id']
        account_name = data['user']['screen_name']
        account_avatar = data['user']['profile_image_url']
        more = data['more']
        weibo_list = []
        containerid = re.search('/p/(.*)', more).groups()[0]

        page = 1
        stop = False
        while True:
            if stop:
                break
            logging.info(tag('crawl page {page}'.format(page=page)))
            # card_type 为 9 是博文信息
            resp = blogs_req(containerid, self.uid, page)
            data = cards = resp.json()['data']
            if not data:
                break
            cards = resp.json()['data']['cards']
            for card in cards:
                card_type = int(card['card_type'])
                if card_type != 9:
                    continue
                mblog = card['mblog']
                isTop = mblog.get('isTop')
                logging.info(tag('create_at {c}'.format(c=mblog['created_at'])))
                created_at = formatDate(mblog['created_at'])
                print(created_at, self.blog_update_at, isTop)
                if not isTop:
                    if created_at < self.blog_update_at:
                        stop = True
                        break
                else:
                    if created_at < self.blog_update_at:
                        continue
                mid = mblog['id']
                url = 'https://m.weibo.cn/detail/{mid}'.format(mid=mid)
                text = mblog['text']
                summary = re.sub(r'<.*?>', '', text)[:20]
                weibo_list.append({
                    'mid': mid,
                    'url': url,
                    'summary': summary,
                })
            page += 1
            time.sleep(random.randint(1,2))

        self.data = {
            'account_id': account_id,
            'account_name': account_name,
            'account_avatar': account_avatar,
            'weibo_list': weibo_list,
            'update_at': update_at
        }
        self.err = 0
        self.reason = config.REASON['done']


def formatDate(s):
    if re.match(r"刚刚", s):
        return datetime.now()
    m = re.match(r"(\d+)分钟前", s)
    if m:
        m = m.groups()[0]
        return datetime.now() - timedelta(minutes=int(m))
    
    h = re.match(r"(\d+)小时前", s)
    if h:
        h = h.groups()[0]
        return datetime.now() - timedelta(hours=int(h))
    t = re.match(r"昨天( [0-9:]+)", s)
    if t:
        s = t.groups()[0]
        s = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + s + ':00'
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    if re.match(r"\d{2}-\d{2}", s):
        s = str(datetime.now().year) + '-' + s + ' 00:00:00'
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    if re.match(r"\d{4}-\d{2}-\d{2}", s):
        s += ' 00:00:00'
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def blogs_req(containerid, uid, page):
    url = 'https://m.weibo.cn/api/container/getIndex'
    params = {
        'page_type':'03',
        'page': page,
        'containerid': containerid
    }
    resp = requests.get(url, headers=config.HEADER, params=params)
    return resp

def get_userinfo(uid):
    url = 'https://m.weibo.cn/profile/info?uid={uid}'.format(uid=uid)
    resp = requests.get(url, headers=config.HEADER)
    return resp
