#/***************************#
# @File        : quickStart.py
# @Time        : 2021/04/06 12:47:06
# @AUTHOR      : small_ant
# @Email       : xms.chnb@gmail.com
# @Desc        : sanic learn
# ****************************/

from sanic import Sanic
from sanic.response import json

app = Sanic("hello")


@app.route('/')
async def test(request):
    return json({"key": "value"})

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
