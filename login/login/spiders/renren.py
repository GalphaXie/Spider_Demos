# -*- coding: utf-8 -*-
import scrapy
import re


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/941954027/profile']

    # 重写start_requests方法
    def start_requests(self):
        cookies_str = '''anonymid=jh2smq74-30zxhl; depovince=GW; jebecookies=95c2ecad-01d7-47a7-8b06-3542457373d2|||||; _r01_=1; JSESSIONID=abcfQYEYTGLQOescEqsnw; ick_login=ce4794ae-a5d6-4b01-8906-0dc8bf769b2b; _de=7A7A02E9254501DA6278B9C75EAEEB7A; p=7de510680a128e3f822cc1d01359345a7; first_login_flag=1; ln_uact=13146128763; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; t=4a89a8329fd0fb36a2043874ef8f12747; societyguester=4a89a8329fd0fb36a2043874ef8f12747; id=941954027; xnsid=adbe0784; loginfrom=syshome; ch_id=10050'''
        cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookies_str.split("; ")}
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                cookies=cookie_dict,
                # headers = {"Cookie":cookies_str}
            )

    def parse(self, response):
        # 判断是否请求成功
        ret = re.findall("新用户28763", response.body.decode())
        print(ret)
        yield scrapy.Request(
            "http://www.renren.com/941954027/profile?v=info_timeline",
            callback=self.parse_next
        )

    def parse_next(self, response):
        # 判断是否请求成功
        ret = re.findall("新用户28763", response.body.decode())
        print(ret)
