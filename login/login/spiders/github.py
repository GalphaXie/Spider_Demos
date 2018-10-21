# -*- coding: utf-8 -*-
import scrapy
import re


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        # 准备请求体
        commit = response.xpath("//input[@name='commit']/@value").extract_first()
        utf8 = response.xpath("//input[@name='utf8']/@value").extract_first()
        authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
        formdata = dict(  # 字典的写法,可以如此,不用给key加引号
            commit=commit,
            utf8=utf8,
            authenticity_token=authenticity_token,
            login="noobpythoner",
            password="zhoudawei123"
        )

        # 发送post 请求
        yield scrapy.FormRequest(
            "https://github.com/session",  # url
            formdata=formdata,  # 请求体
            callback=self.parse_login
        )

    def parse_login(self, resposne):
        ret = re.findall("noobpythoner", resposne.body.decode(), re.I)
        print(ret)
