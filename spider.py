# coding: utf8

"""
爬虫
"""

import gevent
gevent.patch_all()

import requests

from gevent import Pool
from lxml import etree
from dbmixin import DBMixin

from config import USER_AGENT, POOL_SIZE


class HTTPError(Exception):

    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url

    def __str__(self):
        return "%s HTTP %s" % (self.self.url, self.status_code)


class URLFetchError(Exception):

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "%s fetch failed!" % self.self.url


class DoubanSpider(DBMixin):

    """" 豆瓣爬虫 """

    def __init__(self):
        self.result = self.db.result_douban
        self.cache = self.db.cache_douban
        self.session = requests.Session()
        self.pool = Pool(size=POOL_SIZE)

    def fetch(self, url, timeout=10, retury_num=3):
        """发起HTTP请求

        @url, str, URL
        @timeout, int, 超时时间
        @retury_num, int, 重试次数
        """
        kwargs = {
            "headers": {"User-Agent" : USER_AGENT},
        }
        kwargs["timeout"] = timeout
        resp = None
        for i in range(retury_num):
            try:
                resp = self.session.get(url, **kwargs)
                if resp.status_code != 200:
                    raise HTTPError(resp.status_code)
                break
            except Exception as exc:
                logging.warn("%s %d failed!\n%s", url, i, str(exc))
                continue
        if resp is None:
            raise URLFetchError(url)
        return resp.content.decode("utf8")

    def extract(self, regx, body, multi=False):
        """直接解析某个元素,xpath语法

        @regx, str, 解析表达式
        @body, unicode or element, 网页源码或元素
        @multi, bool, 是否取多个
        """
        if isinstance(body, unicode):
            body = etree.HTML(body)
        res = body.xpath(regx)
        if multi:
            return res
        return res[0] if res else None


def test():
    """ main """
    spider = DoubanSpider()
    url = "http://www.douban.com/group/26926/"
    resp = spider.fetch(url)
    regx = "//table[@class='olt']/tr/td[@class='title']/a/@href"
    urls = spider.extract(regx, resp, multi=True)
    print urls


if __name__ == "__main__":
    test()
