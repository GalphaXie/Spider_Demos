from pymongo import MongoClient

client = MongoClient(host='127.0.0.1', port=27017)

collection = client["test100"]['t3']

# temp_list = [{"name":"py{}".format(i), "_id":i} for i in range(1000)]
# print(temp_list)
# collection.insert_many(temp_list)
print(list(collection.find({"_id": {"$in": [i for i in range(0, 1000, 100)]}}, {"_id": 0, "name": 1})))
