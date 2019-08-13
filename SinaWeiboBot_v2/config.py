#coding=utf-8
#配置信息
from multiprocessing import cpu_count
import random, os

TASK_LOOP_PID = "/tmp/sinaweibobot.pid"
BLOG_PID =  "/tmp/sinaweibobot_blog.pid"




# 博文抓取每页延时
BLOG_DELAY = 5

# 任务协同并发
REQUEST_CONCURRENCY = 20

# 上报充实次数
REPORT_RETRY = 5
# 每隔几秒调用一次任务接口
FETCH_TASK_DELAY = lambda: random.randint(20, 60)
# 点赞之前访问博文页后的暂停时间
OPERATE_HEART_DELAY = lambda: random.randint(1, 2)
# 转发之前访问博文页后的暂停时间
OPERATE_REPOST_DELAY = lambda: random.randint(1, 2)
# 评论之前访问博文页后的暂停时间 num 为评论字数
OPERATE_COMMENT_DELAY = lambda num: num * random.uniform(0.2, 0.5)
# 访问热搜随机词数
READ_HOTWORD_COUNT = lambda: random.randint(1, 3)
# 访问热搜随机页数
READ_PAGE_COUNT = lambda: random.randint(2, 5)
# 访问热搜热门页随机页数
READ_HOT_PAGE_COUNT = lambda: random.randint(1, 3)
# 访问热搜实时页随机页数
READ_REALTIME_PAGE_COUNT = lambda: random.randint(1, 3)
# 访问热搜每页延时
OPERATE_HOTWORD_DELAY = lambda: random.randint(5, 10)
# 获取任务后的执行延时（等待网络初始化）
START_TASK_DELAY = 2
# 博文抓取最大页码
BLOG_MAX_PAGE = 10000
# 请求异常重试次数
RETRY = 3
# 请求超时时间 
REQUEST_TIMEOUT = 10
# 登录验证码错误重试次数
LOGIN_VERIFY_RETRY = 3



TASK_URL = 'http://127.0.0.1:8888/task'
TASK_BACK_URL = 'http://127.0.0.1:8888/taskback'

FAST_TASK_URL = 'http://127.0.0.1:8001/api/v1/task/assign'
FAST_TASK_BACK_URL = 'http://127.0.0.1:8001/api/v1/task/report'
REPORT_IP_URL = 'http://127.0.0.1:8888/api/v1/task/ip_check'


# FAST_TASK_URL = 'http://master.ab.local/api/v1/task/assign'
# FAST_TASK_BACK_URL = 'http://master.ab.local/api/v1/task/report'
# REPORT_IP_URL = 'http://master.ab.local/api/v1/task/ip_check'
# TASK_URL = 'http://master.ab.local/api/v1/task/assign'
# TASK_BACK_URL = 'http://master.ab.local/api/v1/task/report'

# 打码服务相关配置
VERIFY_URL = 'http://router.ab.local/cgi-bin/luci/api/ocr'


COMMENTS_FILE = os.path.abspath(os.path.dirname(__file__)) + '/words.txt'
LOG_FILE = './logBot.log'
LOG_FILE_BLOGBOT = './logBlogBot.log'
CACHE_DIR = os.path.abspath(os.path.dirname(__file__)) + '/Cache'
# LOG_LEVEL = 'ERROR'
LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'DEBUG'

# tornado
TORNADO_CLIENT = 'tornado.curl_httpclient.CurlAsyncHTTPClient'
# TORNADO_CLIENT = 'tornado.simple_httpclient.SimpleAsyncHTTPClient'
MAX_CLIENTS = 50

PV_HEADER = {
    'User-Agent': 'spider',
}
HEADER = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://m.weibo.cn/',
    'Connection': 'keep-alive',
}
REASON = {
    'done': 'done',
    'ip_forbidden': 'ip_forbidden',
    'bad_vpn': 'bad_vpn',
    'bot_run_error': 'bot_run_error',
    'bad_account': 'bad_account',
    'account_expired': 'account_expired',
    'timeout': 'timeout',
    'blog_not_found': 'blog_not_found',
    'account_forbidden': 'account_forbidden',
    'account_not_found': 'account_not_found',
    'task_not_support': 'task_not_support',
    'content_repeat': 'content_repeat',
    'frequent_login': 'frequent_login',
    'heart_operate_fail': 'heart_operate_fail',
    'frequent_comment': 'frequent_comment',
    'frequent_repost': 'frequent_repost',
    'only_allows_fans_comment': 'only_allows_fans_comment',
    'account_forbidden_originally': 'account_forbidden_originally',
    'net_err': 'net_err',
    'no_permission': 'no_permission',
    'censor_forbidden': 'censor_forbidden',
}
UA = [
    # # pc
    # # chrome60 window10
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    # # firefox 54 window10
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    # # Safari 12 mac
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15	',
    # # 360
    # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; 360SE)',

    # mobile
    'Mozilla/5.0 (Linux; Android 6.0.1; CPH1607 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',

]



