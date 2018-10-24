# item 对象的封装


class Item(object):
    '''框架内置Item对象'''

    def __init__(self, data):
        # data表示传入的数据
        self._data = data  # 设置为简单的私有属性

    @property
    def data(self):
        '''对外提供data进行访问，一定程度达到保护的作用'''
        return self._data


if __name__ == '__main__':
    """
    演示:1.property 的只读特性　；２．不能赋值特性
    """
    item = Item({"name": 'zhangsan'})
    print(item.data)
    # item.data = {"name": "haha"}

    # 演示：3.可以添加属性和删除
    item.data['age'] = 20
    print(item.data)
    item.data.pop('age')
    print(item.data)
