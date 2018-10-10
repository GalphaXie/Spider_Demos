# -*- coding: utf-8 -*-
# @File : detail.py.py
# @Author : Xie
# @Desc   :
import requests
import re


url = 'https://www.indiegogo.com/projects/atom-a-pocket-sized-3-axis-smartphone-gimbal'
headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

resp = requests.get(url,headers=headers)
html = resp.content.decode()
# print(html)
ret = re.findall(r'"forever_funding_ends_at":.*?,"overview":"(.*?)","overview_image_url"', html, re.S)[0]
print(ret)

"""
"forever_funding_ends_at":null,"overview":"The ATOM is the smallest 3-axis smartphone gimbal with a foldable structure, which provides great portability, rich fantastic functionality and expanded App extensions.\n\nUnlike all other existing 3-axis gimbals on the market which are always huge and troublesome in mounting phones, with ATOM, you can carry it anywhere with ease even put it in your pocket.  In addition, ATOM also provides a series of fantastic functions which enable you to control your filming work with great flexibility.","overview_image_url"





"""