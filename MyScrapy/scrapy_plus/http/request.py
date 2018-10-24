# 封装request对象


class Request(object):
    """框架内置请求对象的分装, 以便引擎调用"""

    def __init__(self, url, method="GET", headers=None, params=None, data=None):
        """
        初始化request对象
        :param url: url地址
        :param method: 请求方法
        :param headers: 请求头
        :param params: 请求的参数
        :param data: 请求体
        """
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
