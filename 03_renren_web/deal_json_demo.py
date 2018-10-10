# coding=utf-8
import requests
import json
from pprint import pprint
url = "https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?start=0&count=18&loc_id=108288"

headers = {
    "Referer": "https://m.douban.com/movie/nowintheater?loc_id=108288",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}

response = requests.get(url,headers=headers)
# print(response.content.decode())

json_str = response.content.decode()
#json.loads #json字符串转化为python类型
ret1 = json.loads(json_str)
# pprint(ret1) #美化打印数据类型
# print(type(ret1))

# json.dumps #把python类型转化为json字符串
# with open("a.txt","w",encoding="utf-8") as f:
#     f.write(json.dumps(ret1,ensure_ascii=False,indent=4))
#

# json.load #实现包含json的类文件对象和python类型的转化
# with open("a.txt","r",encoding="utf-8") as f:
#     ret2 = json.load(f)
# #     ret2 = json.loads(f.read())
#     print(ret2)
#     print(type(ret2))

# json.dump
# with open("b.txt","w",encoding="utf-8") as f:
#     json.dump(ret1,f,ensure_ascii=False,indent=2)
