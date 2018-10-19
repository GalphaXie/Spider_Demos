# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient

client = MongoClient()
collection = client['yangguang']['info']


class YangguangPipeline(object):
    def process_item(self, item, spider):
        item['content'] = self.process_content(item['content'])
        # collection.insert_one(item)  # item 是 Item()对象,并不是真正意义上的字典,所以不能直接存入数据库
        # KeyError:  'YangguangItem does not support field: _id'  # 这个报错(解释: _Id字段下面插入的是 YangguangItem, 不被识别)
        collection.insert_one(dict(item))
        print(item)
        return item

    def process_content(self, content):  # 处理content字段的数据
        content = [re.sub("\xa0|\s", '', i) for i in content]  # 替换content中的 \xa0 和 \s 字符
        content = [i for i in content if len(i) > 0]  # 去除 content 列表中的空字符
        return content


"""
学习套路:
1. 必须要有 process_item 方法, 框架只认识该方法
2. 可以在该方法中再实现别的方法,如 process_content
3. 列表推导式, 可以用来去重; 可以用来只作为if条件判断筛选...可以说很灵活和强大
"""
