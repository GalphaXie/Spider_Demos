from pymongo import MongoClient

# 实例化客户端
client = MongoClient(host='127.0.0.1', port=27017)

# 创建集合
collection = client['test007']['tv']

# 集合操作
# 插入单个数据
# collection.insert_one({'name': '常山赵子龙', 'age': 27})


# 插入多个数据
# insert_many接收一个列表，列表中为所有需要插入的字典
# item_list = [{"name": "name_{}".format(i), "age": i} for i in range(1, 10)]
# print(item_list)
# collection.insert_many(item_list)

# 查询单个
ret = collection.find_one({"name": "常山赵子龙"})
print(type(ret))  # dict
# print(ret)

# 查询多个
ret_list = collection.find({"name": "name_1"})
# print(ret_list)  # <pymongo.cursor.Cursor object at 0x7f5e56457550>
# for ret in ret_list:  # ret_list 是 Cursor 对象,支持遍历;  特点:类似文件读取中的指针
#     print(ret)
#
# for ret in ret_list:
#     print("*" * 50) # 将无法打印,因为 指针 指向最后,下面没有数据.

# 为了解决上面的 问题 , 结合需求可以 对该可迭代对象进行强制的类型转换 -> list , 这样就可以进行多次的遍历操作;
# 但是,也衍生出来新的问题: 数据量很大的时候,列表占用的内存空间较大.
# ret_li = list(ret_list)
# print(ret_li)


# 更新
# 更新单个
# collection.update_one({"name": "name_1"},{"$set":{"age":100}})
# print(list(collection.find({"name": "name_1"})))

# 更新多个
# collection.update_many({"name":"name_2"},{"$set":{"age":200}})
# print(list(collection.find({"name":"name_2"})))

# 删除
# 删除单个
# collection.delete_one({"name":"name_1"})
# print(list(collection.find({"name": "name_1"})))


# 删除多个
# collection.delete_many({"name":"name_2"})
# print(list(collection.find({"name":"name_2"})))
