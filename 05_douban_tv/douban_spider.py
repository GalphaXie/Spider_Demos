# coding=utf-8
import requests
import json


class Douban:
    def __init__(self):
        # self.url_temp = "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18&loc_id=108288"

        self.url_temp_list = [
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18&loc_id=108288",
                "referer": "https://m.douban.com/tv/american"
            },
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?start={}&count=18&loc_id=108288",
                "referer": "https://m.douban.com/tv/british"
            },
        ]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Mobile Safari/537.36"
        }

    def parse_url(self, url):
        print(url)
        resp = requests.get(url, headers=self.headers)
        json_str = resp.content.decode()
        return json_str

    def get_content_list(self, json_str):
        temp_dict = json.loads(json_str)
        return temp_dict["subject_collection_items"]

    def save_content_list(self, content_list):
        with open("douban.txt", "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("保存成功")

    def run(self):  # 实现主要逻辑
        for url_temp in self.url_temp_list:
            self.headers.update({"referer": url_temp["referer"]})  # 更新referer字段
            num = 0
            while True:
                # 1. start_url
                next_url = url_temp["url_temp"].format(num)
                # 2. 发送请求，获取响应
                json_str = self.parse_url(next_url)
                # 3.提取数据
                content_list = self.get_content_list(json_str)
                # 4. 保存
                self.save_content_list(content_list)
                # 5. 构造下一页的url地址，循环 2-5步
                num += 18

                if len(content_list) < 18:  # 当获取的数据列表长度小于18的时候，停止执行
                    break


if __name__ == '__main__':
    douban = Douban()
    douban.run()
