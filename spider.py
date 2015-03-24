# coding: utf8

"""
爬虫
"""

from gevent import monkey
monkey.patch_all()

import time
import random
import logging

import gevent
import requests
from gevent.pool import Pool
from gevent.queue import Queue
from lxml import etree
from dbmixin import DBMixin

from config import (
    GROUP_LIST, GROUP_SUFFIX, USER_AGENT,
    POOL_SIZE, RULES, MAX_PAGE, WATCH_INTERVAL
)
from utils import Timer, ProxyManager


class HTTPError(Exception):

    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url

    def __str__(self):
        return "%s HTTP %s" % (self.url, self.status_code)


class URLFetchError(Exception):

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "%s fetch failed!" % self.self.url


class DoubanSpider(DBMixin):

    """" 豆瓣爬虫 """

    def __init__(self, proxy_manager=None):
        self.result_page = self.db.result_page
        self.result_topic = self.db.result_topic
        self.cache = self.db.cache_page
        self.session = requests.Session()

        self.group_list = GROUP_LIST
        self.rules = RULES
        self.interval = WATCH_INTERVAL

        self.pool = Pool(size=POOL_SIZE)
        self.page_queue = Queue()
        self.topic_queue = Queue()

        self.proxy_manager = proxy_manager

    def fetch(self, url, timeout=10, retury_num=10):
        """发起HTTP请求

        @url, str, URL
        @timeout, int, 超时时间
        @retury_num, int, 重试次数
        """
        kwargs = {
            "headers": {
                "User-Agent": USER_AGENT,
                "Referer": "http://www.douban.com/"
            },
        }
        kwargs["timeout"] = timeout
        resp = None
        for i in range(retury_num):
            try:
                # 是否启动代理
                if self.proxy_manager is not None:
                    kwargs["proxies"] = {"http": self.proxy_manager.get_proxy()}
                resp = self.session.get(url, **kwargs)
                if resp.status_code != 200:
                    raise HTTPError(resp.status_code, url)
                break
            except Exception as exc:
                logging.warn("%s %d failed!\n%s", url, i, str(exc))
                time.sleep(2)
                continue
        if resp is None:
            raise URLFetchError(url)
        return resp.content.decode("utf8")

    def extract(self, regx, body, multi=False):
        """解析元素,xpath语法

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

    def run(self):
        """run
        """
        all_greenlet = []
        # 定时爬取
        for group_url in self.group_list:
            # timer = Timer(random.randint(0, self.interval), self.interval)
            timer = Timer(random.randint(0, 2), self.interval)
            greenlet = gevent.spawn(
                timer.run, self._init_page_tasks, group_url)
            all_greenlet.append(greenlet)
        # 生产 & 消费
        all_greenlet.append(gevent.spawn(self._page_loop))
        all_greenlet.append(gevent.spawn(self._topic_loop))
        # 重载代理
        proxy_timer = Timer(600, 600)
        all_greenlet.append(
            gevent.spawn(proxy_timer.run(self.reload_proxies)))
        gevent.joinall(all_greenlet)

    def reload_proxies(self):
        """重新加载代理
        """
        self.proxy_manager.reload_proxies()

    def _init_page_tasks(self, group_url):
        """初始化页面任务

        @group_url, str, 小组URL
        """
        for page in range(MAX_PAGE):
            base_url = "%s%s" % (group_url, GROUP_SUFFIX)
            url = base_url % (page * 25)
            self.page_queue.put(url)

    def _page_loop(self):
        """page loop
        """
        while 1:
            page_url = self.page_queue.get(block=True)
            gevent.sleep(1)
            self.pool.spawn(self._crawl_page, page_url)

    def _topic_loop(self):
        """topic loop
        """
        while 1:
            topic_url = self.topic_queue.get(block=True)
            self.pool.spawn(self._crawl_detail, topic_url)

    def _crawl_page(self, url):
        """爬取帖子

        @url, str, 当前页面URL
        """
        logging.info("processing page: %s" % url)
        html = self.fetch(url)
        topic_urls = self.extract(
            self.rules["url_list"], html, multi=True)
        # 找出新增的帖子URL
        diff_urls = self._diff_urls(topic_urls)
        if not diff_urls:
            logging.info("%s no update ..." % url)
            return
        logging.info("%s new add : %d" % (url, len(diff_urls)))
        topic_list = self.extract(
            self.rules["topic_item"], html, multi=True)
        # 获取每一页的信息
        topics = self._get_page_info(topic_list)
        # 过滤重复
        topics = self._filter_topics(topics, diff_urls)
        # 保存每页的信息
        self.result_page.insert(topics)
        # 初始化帖子任务
        self._init_topic_tasks(diff_urls)
        # 更新缓存
        self._update_cache(diff_urls)

    def _get_page_info(self, topic_list):
        """获取每一页的帖子基本信息

        @topic_list, list, 当前月的帖子项
        """
        topics = []
        # 第一行是标题头,舍掉
        for topic_item in topic_list[1:]:
            topic = {}
            topic["title"] = self.extract(self.rules["title"], topic_item)
            topic["author"] = self.extract(self.rules["author"], topic_item)
            topic["reply"] = self.extract(self.rules["reply"], topic_item) or 0
            topic["last_reply_time"] = self.extract(
                self.rules["last_reply_time"], topic_item)
            topic["url"] = self.extract(self.rules["url"], topic_item)
            topic["got_time"] = time.time()
            topics.append(topic)
        return topics

    def _filter_topics(self, topics, diff_urls):
        """过滤重复帖子

        @topics, list, 当前页所有帖子信息
        @diff_urls, list, 新增的帖子URL
        """
        return [
            topic for topic in topics
            if topic["url"] in diff_urls
        ]

    def _diff_urls(self, topic_urls):
        """过滤重复帖子URL

        @topic_urls, list, 当前页所有帖子URL
        """
        # 与缓存比较
        cache_urls = []
        cursor = self.cache.find()
        for item in cursor:
            cache_urls.extend(item["urls"])
        # 找出新增的URL
        diff_urls = list(set(topic_urls) - set(cache_urls))
        return diff_urls

    def _init_topic_tasks(self, topic_urls):
        """初始化帖子任务

        @topic_urls, list, 当前页面帖子的URL
        """
        for url in topic_urls:
            self.topic_queue.put(url)

    def _update_cache(self, diff_urls):
        """更新缓存

        @diff_urls, list, 新增的帖子URL
        """
        self.cache.insert(
            {"got_time": time.time(), "urls": diff_urls})

    def _crawl_detail(self, url):
        """爬取每个帖子的详情

        @url, str, 每个帖子的URL
        """
        logging.info("processing topic: %s" % url)
        html = self.fetch(url)
        # 获取每一页的信息
        topic = self._get_detail_info(html, url)
        topic["url"] = url
        topic["got_time"] = time.time()
        # 保存每页的信息
        self.result_topic.insert(topic)

    def _get_detail_info(self, html, url):
        """获取帖子详情

        @html, str, 页面
        """
        topic = {}
        title = self.extract(
            self.rules["detail_title"], html)
        topic["title"] = title.strip()
        topic["create_time"] = self.extract(
            self.rules["create_time"], html)
        topic["author"] = self.extract(
            self.rules["detail_author"], html)
        topic["content"] = '\n'.join(
            self.extract(self.rules["content"], html, multi=True))
        return topic


def main():
    """ main """
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s-%(message)s]",
        level=logging.INFO)
    proxy_manager = ProxyManager("./proxy_list.txt", 30)
    spider = DoubanSpider(proxy_manager)
    spider.run()


if __name__ == "__main__":
    main()
