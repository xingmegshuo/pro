"""
/***************************
@File        : celery1.py
@Time        : 2021/04/07 13:40:45
@AUTHOR      : small_ant
@Email       : xms.chnb@gmail.com
@Desc        : celery demo
****************************/
"""


from celery.schedules import timedelta
from celery import Celery


class Config:
    BROKER_URL = 'redis://192.168.0.15:6379/5'
    CELERY_RESULT_BACKEND = 'redis://192.168.0.15:6739/6'
    CELERY_TIMEZONE = 'Asia/Shanghai'


app = Celery('celery-tasks')
app.config_from_object(Config)


@app.task(queue='for_task_collect')  # 第一个队列
def println():
    print("thanks")
    return "success"


@app.task(queue='for_task_add')  # 第二个队列
def add(x, y):
    print(x + y, "result")
    return x + y
