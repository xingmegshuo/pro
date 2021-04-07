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
import websockets


async def echo(websocket, path):
    async for message in websocket:
        message = "I got your message: {}".format(message)
        await websocket.send(message)


print("服务开启：")
asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
