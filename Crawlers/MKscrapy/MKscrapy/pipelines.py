# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from MKscrapy import settings
import json
import time
import pymongo


# 同时写到文件与database中
class MkscrapyPipeline(object):
    today = ''  # this is also the collection name of the mongodb

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGODB_URI"),
            mongo_db=crawler.settings.get("MONGODB_DBNAME")
        )

    def open_spider(self, spider):
        self.today = 'd' + time.strftime('%Y_%m_%d',
                                         time.gmtime(time.time()))  # 获取当天的UTC时间，考虑到mongodb的命名规则，采取以下格式：d年_月_日
        self.file = open('files_gotten/products_json/Sale_Products_' + self.today + '.jl', 'w')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.file.close()
        self.client.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), indent=4) + '\n'  # 加上indent后比较美观
        self.file.write(line)
        # if this product exists in the db, it will not be inserted again
        self.db[self.today].update({'style_id': item['style_id']}, {'$set': dict(item)}, True)
        return item
