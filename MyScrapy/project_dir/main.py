# -*- coding: utf-8 -*-


from scrapy_plus.core.engine import Engine  # 导入引擎

if __name__ == '__main__':
    engine = Engine()  # 创建引擎对象
    engine.start()  # 启动引擎
