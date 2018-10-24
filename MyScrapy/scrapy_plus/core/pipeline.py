# 管道对象的封装


class Pipeline:
    """完成对管道对象的封装, 负责处理item数据"""

    def process_item(self, item):
        """
        对item进行处理
        :param item:
        :return:
        """
        print('item: ', item.data)
        return item
