import requests
import re
import json


class Krspider:

    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        }
        self.url = "http://36kr.com/"

    def parse(self):
        """
        发送请求获取响应
        :return:
        """
        resp = requests.get(self.url, headers=self.headers)
        resp = resp.content.decode()
        return resp

    def get_data(self, resp_data):
        """
        提取数据
        :return:
        """
        json_str = re.findall("<script>var props=(.*?),locationnal=", resp_data)[0]
        # print(json_str)

        dict_data = json.loads(json_str)

        data_list = dict_data["feedPostsLatest|post"]

        li_data = []
        for data in data_list:
            if data.get("_type"):
                item = {}

                # 获取标题
                item["title"] = data["title"]

                # 获取链接
                item["href"] = "p" if data["_type"] == "post" else data["_type"]
                item["href"] = "http://36kr.com/" + item["href"] + "/" + data["id"]

                item = json.dumps(item, ensure_ascii=False)
                print(item)
                li_data.append(item)

        return li_data

    def save_data(self, li_data):
        """
        保存数据
        :param li_data:
        :return:
        """
        with open('36Kr_news_title', 'w') as f:
            for data in li_data:
                # print(data)
                f.write(data)
                f.write('\n')

    def run(self):
        resp_data = self.parse()
        li_data = self.get_data(resp_data)
        self.save_data(li_data)





#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
# url = "http://36kr.com/"
# resp = requests.get(url, headers=headers)
#
# ret = re.findall("<script>var props=(.*?)</script>", resp.content.decode())[0]
#
# with open("36kr.json", "w", encoding="utf-8") as f:
#     f.write(ret)
#
# dict_ret = json.loads(ret)
# print(ret)


if __name__ == '__main__':
    kr = Krspider()
    kr.run()

