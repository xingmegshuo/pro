"""
/***************************
@File        : task_search.py
@Time        : 2021/04/07 13:46:16
@AUTHOR      : small_ant
@Email       : xms.chnb@gmail.com
@Desc        : task status
****************************/
"""


from celery1 import add, println  # 导入我们的任务函数add
for i in range(1, 100):
    println.delay(i)
    add.delay(i, 10)