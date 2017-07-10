# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem


# 去重复的 company
class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['info_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['info_id'])
            return item


class ItjuziSpiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db,mongo_rs,mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_rs = mongo_rs
        self.mongo_col = mongo_col


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_rs = crawler.settings.get('MONGO_REPLICA'),
            mongo_col = crawler.settings.get('MONGO_COL')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,replicaset=self.mongo_rs)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not item['info_id']:
            raise DropItem('item info_id is null.{0}'.format(item))
        else:
            company = dict(item)
            self.db[self.mongo_col].insert(company)
        return item
