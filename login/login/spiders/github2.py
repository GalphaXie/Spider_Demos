# -*- coding: utf-8 -*-
import scrapy
import re


class Github2Spider(scrapy.Spider):
    name = 'github2'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        # 准备post的数据
        formdata = {
            "login": "noobpythoner",
            "password": "zhoudawei123"
        }
        # 发送请求
        yield scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.parse_login
        )

    def parse_login(self, response):
        ret = re.findall("noobpythoner", response.body.decode(), re.I)
        print(ret)
