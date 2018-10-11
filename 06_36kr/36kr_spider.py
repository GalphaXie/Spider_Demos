# -*- coding: utf-8 -*-
# @File : 36kr_spider.py
# @Author : Xie
# @Desc   : 主要演示: json 报错问题的处理
import json
import re
from pprint import pprint

import requests

url = 'https://36kr.com/'


# 发送请求,获取响应
html_str = requests.get(url).content.decode(encoding='utf-8')


# 数据处理
# ret = re.findall(r'<script>var props=(.*?)</script>', html_str, re.S)
ret = re.findall(r'<script>var props=(.*?),locationnal=', html_str, re.S)
if not len(ret):
    print('匹配数据异常')

# data_dict = json.loads(ret[0])
#
# print(data_dict)

# 报错: json.decoder.JSONDecodeError: Extra data: line 1 column 114722 (char 114721)

# 思路: 为了更加直观的显示,我们这里采取写入文件查看

with open('data.json', 'w', encoding='utf-8') as f:
    # f.write(json.loads(ret[0]))  # 写法错误
    f.write(ret[0])

data_dict = json.loads(ret[0])
pprint(data_dict)