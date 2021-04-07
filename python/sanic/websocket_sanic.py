"""
/***************************
@File        : websocket_sanic.py
@Time        : 2021/04/07 16:15:15
@AUTHOR      : small_ant
@Email       : xms.chnb@gmail.com
@Desc        : sanic for websockets
**************************** /
"""
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

app = Sanic("websocket_example")


@app.websocket('/feed')
async def feed(request, ws):
    # print("server start !!!")
    while True:
        data = await ws.recv()
        # print('Received: ' + data)
        data = 'hello!'+str(data)
        # print('Sending: ' + data)
        await ws.send(data)
    # print("server exit !!!")


if __name__ == "__main__":
    app.config.WEBSOCKET_MAX_QUEUE = 32
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
