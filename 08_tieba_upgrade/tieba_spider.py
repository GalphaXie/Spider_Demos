# 需求：爬取任意百度贴吧的列表页标题和链接地址; 以及每一个帖子(详情页)内的图片
# 思路: 使用chrome浏览器中低版本的手机端,找到百度贴吧极速版的入口,使用 xpath 来提取数据
"""
https://tieba.baidu.com/mo/q---7EAD792A1FE0B613B16325D0E5802760%3AFG%3D1--1-3-0--2--wapp_1539301430297_582/m?kw=%E6%9D%8E%E6%AF%85&lp=5011&lm=&pn=20



"""
import json
import sys
import time
import random

from lxml import etree
import requests


class TiebaSpider:
    def __init__(self, tieba_name):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
        }
        self.start_url = 'https://tieba.baidu.com/mo/q---7EAD792A1FE0B613B16325D0E5802760%3AFG%3D1--1-3-0--2--wapp_1539301430297_582/m?kw={}&lp=5011&lm=&pn=0'.format(tieba_name)
        self.part_url = 'https://tieba.baidu.com/mo/q---7EAD792A1FE0B613B16325D0E5802760%3AFG%3D1--1-3-0--2--wapp_1539301430297_582/'

    def get_response(self, url):
        print(requests.utils.unquote(url))
        resp = requests.get(url, self.headers)
        # print(resp.content)  # 比对请求结果和 element 中结果的区别
        return resp.content

    def parse_data(self, html_bytes):
        # print(html_bytes.decode('utf-8', 'ignore'))
        html = etree.HTML(html_bytes)
        # 增加处理逻辑: 控制停止爬取的节点
        a_list = html.xpath('//body/div/div[contains(@class, "i")]/a')
        data_list = []
        for a in a_list:
            item = {}
            # url 要拼接
            item['href'] = self.part_url + a.xpath('./@href')[0] if len(a.xpath('./@href')) > 0 else None
            item['title'] = a.xpath('./text()')[0] if len(a.xpath('./@href')) > 0 else None
            item["img_list"] = self.get_img_list(item["href"], [])
            # print(item)
            data_list.append(item)
        # 获取下一页的url地址
        next_url = self.part_url + html.xpath('//a[contains(text(), "下一页")]/@href')[0] if len(
            html.xpath('//a[contains(text(), "下一页")]/@href')) > 0 else None
        return data_list, next_url

    def get_img_list(self, detail_url, img_list):
        # 1.发送请求,获取响应
        detail_html_str = self.get_response(detail_url)
        # 2.提取数据
        detail_html = etree.HTML(detail_html_str)
        img_list += detail_html.xpath("//img[@class='BDE_Image']/@src")

        # 详情页下一页的url地址
        next_url = detail_html.xpath("//a[text()='下一页']/@href")
        next_url = self.part_url + next_url[0] if len(next_url) > 0 else None
        if next_url is not None:  # 当存在详情页的下一页，请求
            return self.get_img_list(next_url, img_list)

        # else不用写
        img_list = [requests.utils.unquote(i).split("src=")[-1] for i in img_list]
        return img_list

    def save_content(self, data):
        with open('tieba.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
        print(data)
        print('保存成功')

    def run(self):
        # 获取url, 这里的url的最后一页数量不确定,所以不能 构造 url 列表
        next_url = self.start_url

        while next_url is not None:
            # 发送请求,获取响应
            html = self.get_response(next_url)

            # 数据处理
            data_list, next_url = self.parse_data(html)

            # 保存
            self.save_content(data_list)

            time.sleep(random.randint(1, 4) * 0.5)


if __name__ == '__main__':
    # print('请在终端按照格式[python3 tieba_spider.py 贴吧名],例如[python3 tieba_spider.py "李毅"]运行该程序')
    # tieba_name = sys.argv[1]
    tieba_name = '武汉'
    spider = TiebaSpider(tieba_name)
    spider.run()
