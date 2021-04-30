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
import json
import time


async def hello(uri, i):
    async with websockets.connect(uri) as websocket:
        await websocket.send("look")
        user = await websocket.recv()
        print(user, '个用户')
        if int(user) > 1:
            print("happy for you ")
        b = await websocket.recv()
        print(b)
        time.sleep(10)
        await websocket.send("exit")


async def echo(uri, i):
    await hello(uri, i)


loop = asyncio.get_event_loop()

loop.run_until_complete(echo('ws://localhost:4321', 'bob'))
# loop.run_forever()
