import json
import sys

import requests


class FanyiSpider:

    def __init__(self, query_string):
        self.url = 'https://fanyi.baidu.com/basetrans'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'
        }
        self.query = query_string
        self.langdetect_url = 'https://fanyi.baidu.com/langdetect'

    def get_post_data(self):
        # 1.url
        # 2.发送请求,获取响应
        data = {'query': self.query}
        json_str = self.get_response(self.langdetect_url, data)
        # 3.处理数据
        lan = json.loads(json_str)['lan']
        to = 'en' if lan == 'zh' else 'zh'
        post_data = {
            'query': self.query,
            'from': lan,
            'to': to
        }
        return post_data

    def get_response(self, url, post_data):
        response = requests.post(url=url, data=post_data, headers=self.headers)
        return response.content.decode()

    def parse_response(self, resp_str):
        resp_dict = json.loads(resp_str)
        ret = resp_dict["trans"][0]["dst"]
        print('[{}] 翻译结果为=>: {}'.format(self.query, ret))

    def run(self):
        # 1. 获取url

        # 2. 发送post请求,接收响应
        post_data = self.get_post_data()
        resp_json_str = self.get_response(self.url, post_data)

        # 3.解析数据
        self.parse_response(resp_json_str)


if __name__ == '__main__':
    # query_string = sys.argv[1]
    query_string = input('输入文字:')
    fanyi = FanyiSpider(query_string)
    fanyi.run()
