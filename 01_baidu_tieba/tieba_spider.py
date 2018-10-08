import requests


class TiebaSpider(object):

    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.temp_url = 'https://tieba.baidu.com/f?kw=' + tieba_name + '&pn={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }

    def get_url_list(self):
        url_list = [self.temp_url.format(i * 50) for i in range(1000)]
        return url_list

    def get_response(self, url):
        print(url)
        res = requests.get(url, headers=self.headers)
        return res.content.decode()

    def save_html(self, page_num, html_str):
        file_path = '{}-第{}页.html'.format(self.tieba_name, page_num)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_str)
        print('保存成功')

    def main(self):
        # 生成url列表
        url_list = self.get_url_list()

        # 发送请求,获取响应
        for url in url_list:
            html_str = self.get_response(url)
            # 保存网页
            page_num = url_list.index(url) + 1
            self.save_html(page_num, html_str)


if __name__ == '__main__':
    name = input('请输入百度贴吧中的贴吧名:')
    tieba = TiebaSpider(name)
    tieba.main()
