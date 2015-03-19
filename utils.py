#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class Timer(object):
    """定时器，定时执行指定的函数

    """

    def __init__(self, start, interval):
        """
        @start, int, 延迟执行的秒数
        @interval, int, 每次执行的间隔秒数
        """
        self.start = start
        self.interval = interval

    def run(self, func, *args, **kwargs):
        """运行定时器

        @func, callable, 要执行的函数
        """
        time.sleep(self.start)
        while True:
            func(*args, **kwargs)
            time.sleep(self.interval)
