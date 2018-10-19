# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class GuokePipeline(object):

    def open_spider(self, spider):  # 在爬虫开启的时候执行一次
        client = MongoClient()
        # self.collection = client["db"]["col"]
        # spider.collection = client["db"]["col"]
        # self.f = open("a.txt","a")

    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item

    def close_spdier(self, spider):  # 爬虫关闭的时候执行一次
        # self.f.close()
        pass
