import time
from . import ActionBase
from config import REASON


class Sleep(ActionBase):

    name = 'sleep'

    def crawl(self, millisecond):
        code, subcode, url, response, data = 0, None, None, None, {}
        time.sleep(int(millisecond) / 1000)
        return code, subcode, url, response, data