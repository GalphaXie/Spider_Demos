# -*- coding: utf-8 -*-
import scrapy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['http://suning.com/']

    def parse(self, response):
        pass
