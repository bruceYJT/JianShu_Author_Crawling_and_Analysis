# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter


class JianshuSpiderPipeline:
    def process_item(self, item, spider):
        return item

class UserMongoPipeline(object):
    collection_name = 'user'

    def __init__(self,mongo_host,mongo_db):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_host = crawler.settings.get('MONGO_HOST'),
            mongo_db = crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        self.db[self.collection_name].update({'slug': item['slug']}, {'$setOnInsert': item}, upsert=True)
        return item