import requests
import config

Request = requests.Request

class Session(requests.sessions.Session):

    def request(self, method, url, **kwargs):
        kwargs.setdefault('timeout', config.REQUEST_TIMEOUT)
        return super(Session, self).request(method, url, **kwargs)

def get(url, params=None, **kwargs):
    kwargs.setdefault('timeout', config.REQUEST_TIMEOUT)
    return requests.api.get(url, params=params, **kwargs)

def post(url, data=None, json=None, **kwargs):
    kwargs.setdefault('timeout', config.REQUEST_TIMEOUT)
    return requests.api.post(url, data=data, json=json, **kwargs)

def session():
    return Session()