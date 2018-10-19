# -*- coding: utf-8 -*-
import scrapy


class GkSpider(scrapy.Spider):
    name = 'gk'
    allowed_domains = ['www.guokr.com']
    start_urls = ['http://www.guokr.com/']

    def parse(self, response):
        pass
