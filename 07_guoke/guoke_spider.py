# -*- coding: utf-8 -*-
# @File : guoke_spider.py
# @Author : Xie
# @Desc   :  如果findall 需要同时匹配两个(),那么就会变成 元祖的形式 放在列表中; 但是在json处理数据的时候,元祖可以直接处理成 数组 形式, 并不会报错.
import time

'''
url = 'https://www.guokr.com/ask/highlight/?page=1'
'''
import json
import re

import requests


class GuokrSpider:
    def __init__(self):
        self.temp_url = 'https://www.guokr.com/ask/highlight/?page={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

    def get_url_list(self):
        return [self.temp_url.format(i) for i in range(1, 101)]

    def get_response(self, url):
        html_str = requests.get(url, self.headers)
        return html_str.content.decode(encoding='utf-8')

    def save_data(self, data):
        with open('data_test.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.write('\n')

    def run(self):
        # 1.获取url列表
        url_list = self.get_url_list()

        for url in url_list:
            print(url)
            # 2.发送请求,获取响应
            try:
                resp = self.get_response(url)
            except Exception as e:
                print('请求异常: %s' % e)
                continue
            # 3.提取数据
            '''<h2><a target="_blank" href="https://www.guokr.com/question/541776/">电子可以相对原子核静止不动嘛？</a></h2>'''
            ret = re.findall(r'<h2><a target="_blank" href="(.*?)">(.*?)</a></h2>', resp, re.S)
            # 4.保存
            if not len(ret):
                print('提取数据失败')
            for line in ret:
                # self.save_data(list(line))
                self.save_data(line)  #

            time.sleep(1)  # 睡眠1s,爬太快容易出现提取不出来数据...


if __name__ == '__main__':
    guokr = GuokrSpider()
    guokr.run()
