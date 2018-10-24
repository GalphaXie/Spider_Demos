"""
引擎组件
要实现的逻辑:
构造spider中start_urls中的请求
传递给调取器进行保存，之后从中取出
取出的request对象交给下载的进行下载，返回response
response交给爬虫模块进行解析，提取结果
如果结果是request对象，重新交给调度器，如果结果是item对象，交给管道处理
"""

from scrapy_plus.http.request import Request  # 导入Request对象

from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline
from .spider import Spider


class Engine(object):
    '''
    a. 对外提供整个的程序的入口
    b. 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    '''

    def __init__(self):
        """实例化其他各个组件"""
        self.spider = Spider()  # 接收爬虫对象
        self.scheduler = Scheduler()  # 初始化调度器对象
        self.downloader = Downloader()  # 初始化下载器对象
        self.pipeline = Pipeline()  # 初始化管道对象

    def start(self):
        '''提供程序启动入口, 启动整个引擎'''
        self._start_engine()

    def _start_engine(self):
        '''依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)'''
        # 1. 爬虫模块发出初始请求:调用爬虫的方法
        start_request = self.spider.start_requests()

        # 2. 把初始请求添加给调度器(队列)
        self.scheduler.add_request(start_request)
        # 3. 从调度器获取请求对象，准备交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        # 4. 利用下载器发起请求
        response = self.downloader.get_response(request)

        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        result = self.spider.parse(response)
        # 6. 判断结果对象
        # 6.1 如果是请求对象，那么就再交给调度器
        if isinstance(result, Request):
            self.scheduler.add_request(result)
        # 6.2 否则，就交给管道处理
        else:
            self.pipeline.process_item(result)
