import sys
from multiprocessing import Pool, cpu_count, freeze_support

from lxml import etree

from . import Request


class Spider:
    """Spider class"""

    name = 'simspider'
    start_urls = []
    pool_size = cpu_count()

    def __init__(self):
        """__init__ setting properties"""
        setattr(self, 'name', self.name)
        # check start_urls is exist
        if not getattr(self, 'start_urls', None):
            raise ValueError('spider must define start_urls')

    def start_request(self):
        """start_requests yield url from start_urls return Request object"""
        for url in self.start_urls:
            yield Request(
                url=url,
                config=getattr(self, 'config', None),
                headers=getattr(self, 'headers', None),
                callback=self.parse,
                **getattr(self, 'kwargs', {}))

    def parse(self, res):
        """parse use must be implement this method"""
        raise NotImplementedError

    @classmethod
    def start(cls):
        instance = cls()
        requests = list(instance.start_request())
        cls._callback(requests)

    @classmethod
    def _callback(cls, requests):
        """_callback
        request url with multi process
        """
        results = []
        if isinstance(requests, list):
            for request in requests:
                for r in request():
                    results.append(r)
        elif isinstance(requests, Request):
            requests()
        for result in results:
            if result is not None:
                cls._callback(result)

    def e_html(self, html):
        return etree.HTML(html)
