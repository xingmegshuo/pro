"""
/***************************
@File        : clients.py
@Time        : 2021/04/07 11:28:47
@AUTHOR      : small_ant
@Email       : xms.chnb@gmail.com
@Desc        : websocket for cli
****************************/
"""


import asyncio
import websockets


async def hello(uri, i):
    async with websockets.connect(uri) as websocket:
        # 发送给服务端我是哪一个连接
        await websocket.send(str(i))
        # 服务端返回消息
        recv_text = await websocket.recv()
        print(recv_text)


async def echo(sem, uri, i):
    async with sem:
        await hello(uri, i)


loop = asyncio.get_event_loop()
# 任务列表
tasks = []
# 设置最大同时连接数
sem = asyncio.Semaphore(500)
# 模拟多少个请求
for i in range(1000):
    task = asyncio.ensure_future(echo(sem, 'ws://localhost:4321/', i))
    tasks.append(task)

# 执行任务
loop.run_until_complete(asyncio.wait(tasks))
