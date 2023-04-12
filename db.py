# -*- coding: utf-8 -*-
import pymongo

from env import *


class MyDatabase:
    _db_url = 'mongodb+srv://{user}:{pwd}@{murl}/?retryWrites=true&w=majority'
    _db_name = 'tg'
    _db_table = ''
    _db_url = _db_url.format(user=mongoUser, pwd=mongoPass, murl=mongoUrl)
    _client = None
    _database = None
    _table = None

    def __init__(self, table):
        self._db_table = table
        self._client = pymongo.MongoClient(self._db_url)
        self._database = self._client[self._db_name]
        self._table = self._database[self._db_table]

    def update_session(self, _id, base):
        query = {'$set': {'session': base}}
        self._database['data'].update_one({'_id': _id}, query)

    def get_session(self):
        return self._database['data'].find_one()

    def add_posts_to_database(self, post_list):
        for p in post_list:
            query = {'pid': p.pid}
            if self._table.count_documents(query) == 0:
                x = self._table.insert_one(p.get_dic())
                if utils.is_offline():
                    print(x.inserted_id)

    def get_publish_queue(self):
        return self._table.find({"is_pub": False}).sort('pid', 1)

    def should_update(self, _id):
        query = self._table.find_one({}, sort=[('pid', -1)])
        if query is None:
            return True
        print(query['pid'])
        if len(list(query)) == 0:
            return True
        last_id = query['pid']
        return _id > last_id

    def add_to_db(self, mList):
        for p in mList:
            query = {'pid': p.pid}
            if self._table.count_documents(query) == 0:
                self._table.insert_one(p.get_dic())
                # print(x.inserted_id)

    def set_published(self, tid, eid):
        query = {'$set': {'is_pub': True, 'pub_id': eid}}
        self._table.update_one({'pid': tid}, query)
