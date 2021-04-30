"""
/***************************
@File        : client.py
@Time        : 2021/04/07 11:23:49
@AUTHOR      : small_ant
@Email       : xms.chnb@gmail.com
@Desc        : websocket server
****************************/
"""

import asyncio
import json

import websockets


STATE = {"value": 0}

# 保存所有在线客户端
USERS = {}


# 注册客户端
async def register(websocket):
    USERS[websocket] = len(USERS) + 1
    print(USERS)


# 注销客户端


async def unregister(websocket):
    del USERS[websocket]
    print(USERS)


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    while True:
        # 迭代websocket以不断接收消息，此处要求对象实现了 __iter__()、__await__()、 __aenter__()、 __aexit__() 方法。
        async for message in websocket:
            if message == 'exit':
                await unregister(websocket)
                break
            if message == 'look':
                await websocket.send(str(len(USERS)))
                if USERS[websocket] == 1:
                    print("发送1")
                    await websocket.send("hello first")
                if USERS[websocket] == 2:
                    print("发送2")
                    await websocket.send("hello Send")


start_server = websockets.serve(counter, "localhost", 4321)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
