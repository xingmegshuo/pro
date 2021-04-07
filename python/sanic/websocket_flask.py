"""
/***************************
@File        : websocket_flask.py
@Time        : 2021/04/07 16:55:48
@AUTHOR      : small_ant
@Email       : xms.chnb@gmail.com
@Desc        : flask websocket
****************************/
"""
from flask import Flask
from flask_sockets import Sockets
import datetime
import time
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)


@app.route('/')
def index():
    return 'hello'


@sockets.route('/feed')
def test(ws):
    while not ws.closed:
        msg = ws.receive()
        print(f'i received:{msg}')
        if msg:
            now = datetime.datetime.now().isoformat()
            ws.send(now)
            print(f'i sent:{now}')
            time.sleep(1)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(
        ('0.0.0.0', 8000), application=app, handler_class=WebSocketHandler)
    print('server started')
    server.serve_forever()
