# coding=utf-8
from selenium import webdriver
import time

class DouYu:
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()

    def get_content_list(self): #提取数据
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        content_list = []
        for li in li_list:
            item = {}
            item["title"] = li.find_element_by_xpath("./a").get_attribute("title")
            item["anchor"] = li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
            item["watch_num"] = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
            print(item)
            content_list.append(item)

        #提取下一页的元素
        next_url = self.driver.find_elements_by_xpath("//a[@class='shark-pager-next']")
        next_url = next_url[0] if len(next_url)>0 else None
        return content_list,next_url

    def save_content_list(self,content_lsit):#保存
        pass

    def run(self): #实现主要逻辑
        #1. start_url
        #2. 发送请求，获取响应
        self.driver.get(self.start_url)
        #3. 提取数据
        content_list,next_url = self.get_content_list()
        #4.保存
        self.save_content_list(content_list)

        # 5. 下一页数据的提取
        while next_url is not None:
            next_url.click() #页面没有完全加载完，会报错
            time.sleep(3)
            content_list,next_url = self.get_content_list()
            self.save_content_list(content_list)

if __name__ == '__main__':
    douyu = DouYu()
    douyu.run()
