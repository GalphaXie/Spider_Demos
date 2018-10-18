# -*- coding: utf-8 -*-
import urllib.parse

import scrapy


class TxSpider(scrapy.Spider):
    name = 'tx'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?keywords=&tid=0']

    def parse(self, response):
        # 1.提取当前页面的数据
        # 先分组, 再提取
        tr_list = response.xpath(".//table[@class='tablelist']/tr")[1:-1]
        for tr in tr_list:
            item = {}
            item['position_name'] = tr.xpath(".//a/text()").extract_first()
            item['position_href'] = tr.xpath("./td[1]/@href").extract_first()
            item['position_category'] = tr.xpath("./td[2]/text()").extract_first()
            item['need_num'] = tr.xpath("./td[3]/text()").extract_first()
            item['location'] = tr.xpath("./td[4]/text()").extract_first()
            item['publish_date'] = tr.xpath("./td[5]/text()").extract_first()
            # print(item)
            yield item

        # 2. 翻页,请求下一页
        # https://hr.tencent.com/position.php?keywords=&tid=0&start=10#a  第一页网址
        # position.php?keywords=&tid=0&start=10#a  提取出来的
        next_url = response.xpath('.//a[@id="next"]/@href').extract_first()
        if next_url != "javascript:;":
            # 需要拼接url
            # 方法一:
            # next_url += "https://hr.tencent.com/"  # 错误:position.php?keywords=&tid=0&start=10#ahttps://hr.tencent.com/
            # next_url = 'https://hr.tencent.com/' + next_url  # 正确
            # 方法二:
            # next_url = urllib.parse.urljoin(self.start_urls[0], next_url)
            # next_url = urllib.parse.urljoin(response.url, next_url)  # response.url 属性有完整的url # 最好导入 urllib.parse 而不是 urllib
            # yield scrapy.Request(  # 构造request 对象, 通过yield交个引擎
            #     next_url,
            #     callback=self.parse
            # )
            # 方法三: 根据response.url 对next_url进行拼接, 构造请求
            yield response.follow(next_url, callback=self.parse, dont_filter=False)
