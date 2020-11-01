#coding=utf-8
import json, time, logging, random, urllib
import sinaRequests as requests
import config
from . import CreateBaseBot
from utils import tag



containerIndexUrl = 'https://m.weibo.cn/api/container/getIndex'


class HotsearchBot(CreateBaseBot):

    name = 'hotsearch'

    def __init__(self, taskid, params):
        cookies = params['cookies']
        uid = str(params['uid'])
        self.st = params['st']
        super(HotsearchBot, self).__init__(taskid, uid, cookies)

    def crawl(self):
        self.session = self.initSession()
        self.read()
        if not self.err:
            self.reason = config.REASON['done']
            self.err = 0

    def gen_read_task(self):
        # 1-3 个
        # 2-5 页
        # 5-10 秒
        read_count = config.READ_HOTWORD_COUNT()
        self.data = {'read_count': read_count, 'words': []}
        hot_word = get_all_hot_word(session=self.session)
        if not hot_word:
            logging.info(tag('get all hot word fail'))
            self.err = 1
            self.reason = config.REASON['bot_run_error']
            return

        read_word = []
        for i in range(read_count):
            item = random.choice(hot_word)
            read_word.append(item)
            hot_word.remove(item)
        return read_word

    def read(self):
        read_words = self.gen_read_task()
        for w in read_words:
            self.read_word_req(w)

    def read_word_req(self, word_dict):
        page_count = config.READ_PAGE_COUNT()
        hot_page_count = config.READ_HOT_PAGE_COUNT()
        realtime_page_count = config.READ_REALTIME_PAGE_COUNT()
        url = word_dict['scheme']
        word = word_dict['desc']
        params = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.data['words'].append({
            'word': word,
            'count': page_count,
            'hot_page_count': hot_page_count,
            'realtime_page_count': realtime_page_count
        })
        for page_num in range(1, page_count + 1):
            # 请求第一页时首先访问 html 然后请求数据接口
            if page_num == 1:
                hot_word_index_req(self.session, url, word)
            params['page_type'] = 'searchall'
            if page_num != 1:
                params['page'] = page_num
            hot_word_data_req(self.session, params, page_num, word, 1)
            time.sleep(config.OPERATE_HOTWORD_DELAY())

        params['containerid'] = params['containerid'].replace('type=1', 'type=60')
        if 'page' in params:
            del params['page']
        for page_num in range(1, hot_page_count + 1):
            if page_num != 1:
                params['page'] = page_num
            hot_word_data_req(self.session, params, page_num, word, 60)
            time.sleep(config.OPERATE_HOTWORD_DELAY())

        params['containerid'] = params['containerid'].replace('type=1', 'type=61')
        if 'page' in params:
            del params['page']
        for page_num in range(1, realtime_page_count + 1):
            if page_num != 1:
                params['page'] = page_num
            hot_word_data_req(self.session, params, page_num, word, 61)
            time.sleep(config.OPERATE_HOTWORD_DELAY())

# def hot_word_data_hot_req(session, params, page, word):
#     pass

# def hot_word_data_realtime_req(session, params, page, word):
#     pass

def hot_word_index_req(session, url, word):
    logging.info(tag('hot_word_index_req {word}'.format(word=word)))
    resp = session.get(url, headers=config.HEADER)
    # logging.info(tag('hot_word_index_resp word {word} {resp}'.format(
    #     resp=resp.text, word=word)))
    # logging.info(tag('hot_word_index_resp word {word}'.format(word=word)))
    return resp


# 热搜的 实时 综合 热门 数据接口参数中只有 containerid 中 的 type 是不同的
# 综合 type=1
# 热门 type=60
# 实时 type=61
def hot_word_data_req(session, params, page, word, type):
    logging.info(tag('hot_word_data_req word {word}, type {type} page {page} params {params}'.format(
        params=params, page=page, word=word, type=type)))
    resp = session.get(containerIndexUrl, headers=config.HEADER, params=params)
    if resp.json()['ok'] != 1:
        logging.info(tag('hot_word_data_resp word {word} type {type} page {page} {resp}'.format(
            resp=resp.text, page=page, word=word, type=type)))
    return resp

def container_req(**kwargs):
    session = kwargs['session']
    logging.info(tag('container_req'))
    params = {
        'containerid': 231583,
        'page_type': 'searchall'
    }
    resp = session.get(containerIndexUrl, headers=config.HEADER, params=params)
    if resp.json()['ok'] != 1:
        logging.info(tag('container_resp {resp}'.format(resp=resp.text)))

def get_all_hot_word(**kwargs):
    session = kwargs['session']
    params = {
        'containerid': '106003type=25&t=3&disable_hot=1&filter_type=realtimehot'
    }
    resp = session.get(containerIndexUrl, headers=config.HEADER, params=params)
    if resp.json()['ok'] != 1:
        logging.info(tag('hot_word_resp {resp}, {status_code}'.format(
            resp=resp.text, status_code=resp.status_code)))
    cards_hot_word = []
    data = resp.json().get('data')
    if data:
        cards = data.get('cards')
        if cards:
            cards_hot_word = cards[0].get('card_group')
    return cards_hot_word
    # if not cards_hot_word:
    #     return cards_hot_word
    # print(cards_hot_word)



# 首页
# https://m.weibo.cn/search?isnewpage=1
# &extparam=filter_type%3Drealtimehot%26pos%3D0%26c_type%3D51%26q%3D%E4%B8%AD%E5%9B%BD%E5%8F%91%E5%B1%95%E9%AB%98%E5%B1%82%E8%AE%BA%E5%9D%9B%26display_time%3D1553322114
# &luicode=10000011
# &lfid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot
# &containerid=100103type%3D1%26t%3D10%26q%3D%E4%B8%AD%E5%9B%BD%E5%8F%91%E5%B1%95%E9%AB%98%E5%B1%82%E8%AE%BA%E5%9D%9B

# 数据页
# https://m.weibo.cn/api/container/getIndex?isnewpage=1
# &extparam=filter_type%3Drealtimehot%26pos%3D0%26c_type%3D51%26q%3D%E4%B8%AD%E5%9B%BD%E5%8F%91%E5%B1%95%E9%AB%98%E5%B1%82%E8%AE%BA%E5%9D%9B%26display_time%3D1553322114
# &luicode=10000011
# &lfid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot
# &containerid=100103type%3D1%26t%3D10%26q%3D%E4%B8%AD%E5%9B%BD%E5%8F%91%E5%B1%95%E9%AB%98%E5%B1%82%E8%AE%BA%E5%9D%9B
# &page_type=searchall

# 数据页 第二页
# https://m.weibo.cn/api/container/getIndex?isnewpage=1
# &extparam=filter_type%3Drealtimehot%26pos%3D0%26c_type%3D51%26q%3D%E4%B8%AD%E5%9B%BD%E5%8F%91%E5%B1%95%E9%AB%98%E5%B1%82%E8%AE%BA%E5%9D%9B%26display_time%3D1553322114
# &luicode=10000011
# &lfid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot
# &containerid=100103type%3D1%26t%3D10%26q%3D%E4%B8%AD%E5%9B%BD%E5%8F%91%E5%B1%95%E9%AB%98%E5%B1%82%E8%AE%BA%E5%9D%9B
# &page_type=searchall
# &page=2