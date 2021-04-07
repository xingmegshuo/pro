"""
/***************************
@File        : celery1.py
@Time        : 2021/04/07 13:40:45
@AUTHOR      : small_ant
@Email       : xms.chnb@gmail.com
@Desc        : celery demo
****************************/
"""


from celery import Celery
import time
import socket

app = Celery('demo', broker='redis://127.0.0.1:6379/0',
             backend='redis://127.0.0.1:6379/0')


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


@app.task
def add(x, y):
    time.sleep(3)  # 模拟耗时操作
    s = x + y
    print("主机IP {}: x + y = {}".format(get_host_ip(), s))
    return s


if __name__ == '__main__':
    app.start()
    # for i in range(10):
    #     import random
    #     b = random.randint(1, 100000)
    #     add.delay(i, b)
