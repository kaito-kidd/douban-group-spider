# coding: utf8

""" 单例mongo客户端 """

from pymongo import MongoClient

from config import DB_URI, DB_NAME


class DBMixin(object):

    """ mongodb客户端 """

    _client = None

    @property
    def client(self):
        if not self._client:
            self._client = MongoClient(DB_URI)
        return self._client

    @property
    def db(self):
        return self.client[DB_NAME]
