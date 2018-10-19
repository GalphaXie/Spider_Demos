# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookPipeline(object):
    """可以创建多个管道,并且根据不同的逻辑进行不同的处理.比如,if 逻辑  """

    def process_item(self, item, spider):  # 管道专门处理数据的地方;  spider-爬虫实例
        return item  # 必须要return , 否则有多个管道的时候,之后的管道没法取到结果
