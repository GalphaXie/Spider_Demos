# -*- coding: utf-8 -*-
import scrapy


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['http://wz.sun0769.com']
    start_urls = ['http://http://wz.sun0769.com/']

    def parse(self, response):
        pass
