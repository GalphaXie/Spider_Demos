# -*- coding: utf-8 -*-
import scrapy
from ..items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    def parse(self, response):
        # 1.提取当前页数据
        # 1.1 分组
        tr_list = response.xpath('.//div[@class="greyframe"]/table[2]/tr/td/table/tr')
        for tr in tr_list:
            item = YangguangItem()  # 实例化管道对象; 注意导包
            item["num"] = tr.xpath("./td[1]/text()").extract_first()
            item["title"] = tr.xpath("./td[2]/a[2]/text()").extract_first()
            item["href"] = tr.xpath("./td[2]/a[2]/@href").extract_first()
            item["status"] = tr.xpath("./td[3]/span/text()").extract_first()
            item["name"] = tr.xpath("./td[4]/text()").extract_first()
            item["publish_date"] = tr.xpath("./td[5]/text()").extract_first()
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                meta={'item': item}
            )
        # 2.翻页,获取下一页url
        next_url = response.xpath("//a[text()='>']/@href").extract_first()  # 说明:这里对应的网页源码是：&gt;  lxml 可以自动处理
        if next_url:
            # 构造请求对象
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item["img"] = response.xpath("//div[@class='textpic']/img/@src").extract_first()
        item["content"] = response.xpath("//div[@class='c1 text14_2']//text()").extract()
        # print(item)
        yield item  # 这里是把数据交给管道去处理; 这里的 item是管道的实例化对象.
