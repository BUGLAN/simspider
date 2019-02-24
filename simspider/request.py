import time

import requests


class Request:
    """wrapper Request obj"""
    name = 'request'

    CONFIG = {'retries': 3, 'delay': 0, 'timeout': 30}
    METHODS = ['get', 'post']

    def __init__(self,
                 url,
                 method='get',
                 params=None,
                 data=None,
                 config=None,
                 headers=None,
                 cookies=None,
                 callback=None,
                 **kwargs):
        self.url = url
        self.method = method.lower()
        if self.method not in self.METHODS:
            raise ValueError('{} method is not support'.format(self.method))
        if config and isinstance(config, dict):
            self.config = config
        elif config and not isinstance(config, dict):
            raise ValueError('the param config must be dict')
        else:
            self.config = self.CONFIG
        self.params = params
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.callback = callback
        self.kwargs = kwargs

    def __call__(self):
        if self.config.get('delay', 0) > 0:
            time.sleep(self.config.get('delay', 0))
        res = self.download(
            url=self.url,
            method=self.method,
            params=self.params,
            data=self.data,
            headers=self.headers,
            cookies=self.cookies,
            **self.kwargs)
        if self.callback is None:
            return res
        if self.callback(res=res) is not None:
            return list(self.callback(res=res))

    def download(self, url, method, headers, params, data, cookies, **kwargs):
        if method == 'get':
            response = requests.get(
                url=url,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=self.config.get('timeout', 30),
                **kwargs)
        else:
            response = requests.post(
                url=url,
                data=data,
                headers=headers,
                cookies=cookies,
                timeout=self.config.get('timeout', 30),
                **kwargs)
        text = response.text
        a = type('Response', (), {
            'html': text,
            'url': url
        }) if text is not None else None
        return a

    def __str__(self):
        return '<{} {}>'.format(self.method, self.url)
