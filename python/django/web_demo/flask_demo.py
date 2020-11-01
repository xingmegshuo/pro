#!/usr/bin/env python
# coding=utf-8
# Author: 
# Mail: 
# Created Time: 2019年08月18日 星期日 18时31分20秒

'''

flask + docker demo

'''

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello weorld!hello xiaoming!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
