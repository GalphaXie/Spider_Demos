# -*- coding: utf-8 -*-
# @File : tv_spider.py
# @Author : Xie
# @Desc   : 爬取英剧和美剧; 豆瓣的电视剧采取的反爬策略是 refer
import csv
import json
from pprint import pprint

import requests

"""
https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?os=ios&for_mobile=1&callback=jsonp4&start=54&count=18&loc_id=108288&_=0
https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?os=ios&for_mobile=1&callback=jsonp5&start=72&count=18&loc_id=108288&_=0
Referer: https://m.douban.com/tv/american
"""


class DouBanSpider:
    """爬取豆瓣电视剧英剧和美剧数据"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        self.temp_url = None
        self.flag = True

    def get_url_and_add_headers(self):
        """获取url,并且进行不同的headers设置"""
        global choice
        try:
            choice = int(input('请输入数字[0]或[1]来选择[英剧]或[美剧]:'))
            assert choice in [0, 1]
        except Exception:
            print('请按照提示正确输入')
        else:
            if choice == 0:
                self.headers['Referer'] = 'https://m.douban.com/tv/british'
                self.temp_url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?os=ios&start={}&count=18&loc_id=108288'
            elif choice == 1:
                self.headers['Referer'] = 'https://m.douban.com/tv/american'
                self.temp_url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?os=ios&start={}&count=18&loc_id=108288'
            return self.temp_url

    def get_response(self, url, headers):
        try:
            resp = requests.get(url, headers=headers)
            assert resp.status_code == 200
            return resp.content.decode(encoding='utf-8')
        except Exception as e:
            print('响应出错: %s' % e)
            return ''

    def deal_data(self, html_str):
        data_list = []
        try:
            html_dict = json.loads(html_str)
            data_list = html_dict.get("subject_collection_items", None)
        except Exception as e:
            print('处理数据出错: %s' % e)
        return data_list

    def save_data(self, data_dict):
        """字典数据保存为csv文件"""
        file_name = 'british.csv' if choice == 0 else 'american.csv'
        with open(file_name, 'a', encoding='utf-8') as csvfile:
            fieldnames = ["id", "title", "label", "actors", "description", "price", "date", "info", "url", 'uri',
                          "release_date", "cover", "directors", "reviewer_name", 'original_price', 'null_rating_reason',
                          'card_subtitle', 'type', 'subtype', 'has_linewatch', 'year', 'rating', 'interest', 'actions',
                          'forum_info']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.flag:
                writer.writeheader()
                self.flag = False
            writer.writerow(data_dict)
        print('保存成功')

    def run(self):
        """主程序"""
        # 0.获取base_url地址
        base_url = self.get_url_and_add_headers()

        i = 0
        while True:
            i += 1
            # 2.发送请求, 获取响应
            html_str = self.get_response(base_url.format((i - 1) * 18), self.headers)
            if not html_str:
                continue

            # 3.数据处理
            data_list = self.deal_data(html_str)
            if not data_list:
                continue

            # 4.保存数据
            for data_dict in data_list:
                try:
                    self.save_data(data_dict)
                except Exception as e:
                    print('保存数据异常: %s' % e)
                    continue

            if len(data_list) < 18:
                break

            print('爬取成功 %s 页' % i)
        print('全部结束')


if __name__ == '__main__':
    spider = DouBanSpider()
    spider.run()
