# coding=utf-8
"""如果没有下一页,那么<a>的class='shark-pager-next shark-pager-disable shark-pager-disable-next',
而不再是class='shark-pager-next'"""
import json
import time

from selenium import webdriver


class DouyuSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.driver = webdriver.Chrome()
        self.start_url = 'https://www.douyu.com/directory/all/'

    # def get_response(self, url):
    #     response = requests.get(url, self.headers)
    #     return response.content

    def parse_content_list(self):
        li_list = self.driver.find_elements_by_xpath('//ul[@id="live-list-contentbox"]/li')
        content_list = []
        for li in li_list:
            item = {}
            item['title'] = li.find_element_by_xpath('./a').get_attribute("title")
            item['anchor'] = li.find_element_by_xpath('.//span[@class="dy-name ellipsis fl"]').text
            item['watch_num'] = li.find_element_by_xpath('.//span[@class="dy-num fr"]').text
            content_list.append(item)

        # 提取下一页元素
        next_url = self.driver.find_elements_by_xpath('//a[@class="shark-pager-next"]')
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content_list(self, content_list):
        for content in content_list:
            print(content)
            with open('douyu.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write('\n')

    def run(self):
        """主程序"""
        # 1.初始start_url
        next_url = self.start_url

        # 2.请求,响应
        # html_str = self.parse_content_list(next_url)
        self.driver.get(next_url)
        # 3.处理数据
        content_list, next_url = self.parse_content_list()

        # 4.保存
        self.save_content_list(content_list)

        # 5.获取下一页的元素,点击,循环2-5步
        while next_url is not None:  # 这里不和上一步合并是因为这里的url获取方式和上面不同,发送请求和响应也就不同
            next_url.click()  # 页面没有完全加载,会报错
            time.sleep(3)
            content_list, next_url = self.parse_content_list()
            self.save_content_list(content_list)


if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()
