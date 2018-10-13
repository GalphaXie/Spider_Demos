"""

第一页url:http://www.qiushibaike.com/8hr/page/1


- 1.通过队列来传递数据和消息 , 代替之前函数的参数传递;
- 2.可以结合具体情况打乱顺序, 来代替之前有序的循环遍历;
- 3.在 q.get()和q.task_done()之间处理处理业务逻辑之外,需要衔接上 下一个 重要步骤 的 队列,并将当前队列处理结果 put 到 下一个队列中.
- 4.开启线程守护 t.setDaemon(True) 之后, 再开启线程;
- 5.判断结束的节点是:  所有消息队列为空, 再执行接下来的操作. q.join() ;
- 6.注意:区别之前from processing import Queue 和这里的 from queue import Queue , 前者是用在进程间通信; 而这里主要是使用线程优先级队列（ Queue） 的 队列安全锁 特性.

"""
import json
import threading
import time
from queue import Queue

import requests
from lxml import etree


class QiubaiSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.temp_url = 'http://www.qiushibaike.com/8hr/page/{}/'
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_list_queue = Queue()

    def get_url_list(self):
        # return [self.temp_url.format(i) for i in range(1, 14)]
        for i in range(1, 14):
            self.url_queue.put(self.temp_url.format(i))

    def get_response(self):
        """发送请求,获取响应"""
        while True:
            url = self.url_queue.get()
            resp = requests.get(url, self.headers)
            # print(resp)
            if resp.status_code != 200:
                self.url_queue.put(url)  # 这里还可以保证多次发送请求,尽可能的保证成功
            else:
                self.html_queue.put(resp.content)
            self.url_queue.task_done()  # 让队列的计数 -1

    def parse_response(self):
        """解析数据"""
        while True:
            html_bytes = self.html_queue.get()
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
                item['author_gender'] = div.xpath('.//div[@class="author clearfix"]/div/@class')[0].split(" ")[
                    -1].replace('Icon',
                                '') if len(
                    div.xpath('.//div[@class="author clearfix"]/div/@class')) > 0 else None
                item['author_age'] = div.xpath('.//div[@class="author clearfix"]/div/text()')[0] if len(
                    div.xpath('.//div[@class="author clearfix"]/div/text()')) > 0 else None
                item['stats-vote'] = div.xpath('.//div[@class="stats"]/span[@class="stats-vote"]/i/text()')[0] if len(
                    div.xpath('.//div[@class="stats"]/span[@class="stats-vote"]/i/text()')) > 0 else None
                item['stats-comments'] = div.xpath('.//div[@class="stats"]/span[@class="stats-comments"]//i/text()')[
                    0] if len(div.xpath('.//div[@class="stats"]/span[@class="stats-comments"]//i/text()')) > 0 else None

                item_list.append(item)
            self.content_list_queue.put(item_list)
            self.html_queue.task_done()

    def save_content(self):
        while True:
            content_list = self.content_list_queue.get()
            for content in content_list:
                with open('qiubai.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(content, ensure_ascii=False))
                    f.write('\n')
                    print(content)
            print('保存成功')
            self.content_list_queue.task_done()

    def run(self):
        """主程序"""
        thread_list = []
        # 1.获取url
        # url_list = self.get_url_list()
        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)

        # 2.遍历发送请求,获取响应
        for i in range(3):
            t_resp = threading.Thread(target=self.get_response)
            # html_str = self.get_response(url)
            thread_list.append(t_resp)

        # 3.提取数据
        # data_list = self.parse_response(html_str)
        t_content = threading.Thread(target=self.parse_response)
        thread_list.append(t_content)

        # 4.保存数据
        # self.save_content(data_list)
        t_save = threading.Thread(target=self.save_content)
        thread_list.append(t_save)

        # 开启线程
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程,来守护主线程
            t.start()  # 开启子线程

        # 通过队列来设置阻塞效果(这里也可以通过子线程来阻塞)
        for q in [self.url_queue, self.html_queue, self.content_list_queue]:
            q.join()  # 阻塞队列,当队列都为空的时候才可以继续执行接下来的操作


if __name__ == '__main__':
    t1 = time.time()
    qiubai_spider = QiubaiSpider()
    qiubai_spider.run()
    print('total cost: %0.2f' % (time.time() - t1))
