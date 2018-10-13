"""

http://www.qiushibaike.com/8hr/page/1
"""
import json
import time
import requests
from lxml import etree


class QiubaiSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.temp_url = 'http://www.qiushibaike.com/8hr/page/{}/'

    def get_url_list(self):
        return [self.temp_url.format(i) for i in range(1, 14)]

    def get_response(self, url):
        """发送请求,获取响应"""
        resp = requests.get(url, self.headers)
        return resp.content

    def parse_response(self, html_bytes):
        """解析数据"""
        html = etree.HTML(html_bytes)
        div_li = html.xpath('//div[@id="content-left"]/div')
        item_list = []
        for div in div_li:
            item = {}
            item['content'] = " ".join(div.xpath('.//div[@class="content"]//span/text()')) if len(
                div.xpath('.//div[@class="content"]//span/text()')) > 0 else None
            item['author_pic'] = "https:" + div.xpath('.//div[@class="author clearfix"]//img/@src')[0] if len(
                div.xpath('.//div[@class="author clearfix"]//img/@src')) > 0 else None
            item['author_alt'] = div.xpath('.//div[@class="author clearfix"]//img/@alt')[0] if len(
                div.xpath('.//div[@class="author clearfix"]//img/@alt')) > 0 else None
            item['author_gender'] = div.xpath('.//div[@class="author clearfix"]/div/@class')[0].split(" ")[-1].replace('Icon',
                                                                                                              '') if len(
                div.xpath('.//div[@class="author clearfix"]/div/@class')) > 0 else None
            item['author_age'] = div.xpath('.//div[@class="author clearfix"]/div/text()')[0] if len(
                div.xpath('.//div[@class="author clearfix"]/div/text()')) > 0 else None
            item['stats-vote'] = div.xpath('.//div[@class="stats"]/span[@class="stats-vote"]/i/text()')[0] if len(
                div.xpath('.//div[@class="stats"]/span[@class="stats-vote"]/i/text()')) > 0 else None
            item['stats-comments'] = div.xpath('.//div[@class="stats"]/span[@class="stats-comments"]//i/text()')[
                0] if len(div.xpath('.//div[@class="stats"]/span[@class="stats-comments"]//i/text()')) > 0 else None

            item_list.append(item)
        return item_list

    def save_content(self, content_list):
        for content in content_list:
            with open('qiubai.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write('\n')
                print(content)
        print('保存成功')

    def run(self):
        """主程序"""
        # 1.获取url
        url_list = self.get_url_list()
        for url in url_list:
            # 2.发送请求,获取响应
            html_str = self.get_response(url)

            # 3.提取数据
            data_list = self.parse_response(html_str)

            # 4.保存数据
            self.save_content(data_list)

            time.sleep(1)


if __name__ == '__main__':
    qiubai_spider = QiubaiSpider()
    qiubai_spider.run()
