# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

class ProxyMid:
    def process_request(self, request, spider):
        request.meta["proxy"] = "https://124.237.83.14:53281"
