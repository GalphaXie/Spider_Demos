import csv
import datetime
import json
import re
import requests
from lxml import etree


class IndiegogoSpider:
    '''关于www.indiegogo.com的爬虫'''

    def __init__(self):
        self.url = 'https://www.indiegogo.com/private_api/discover'
        self.headers = {
            'content-length': '159',
            'content-type': 'application/json;charset=UTF-8',
            'x-locale': 'en',
            'cookie': 'romref=dir-XXXX; romref_referer_host=; cohort=%7Cdir-XXXX; visitor_id=dd716d4021d8f46a4308baad4237eeb6ed1f6b828e713408e9ef0e1982262213; _session_id=c81824e30aa481de0abeffa8bbc2059a; _ga=GA1.2.1535179021.1539054283; _gid=GA1.2.177772867.1539054283; CookieConsent=-1; __hssrc=1; hubspotutk=4c3ace39cf33b2cb2eee1347db4c651b; recent_project_ids=2417262%262417714; analytics_session_id=10610c566b466519fe4d02f0070b8bdc95dc3a4f3c4af211ab144c6c13d3e58a; __hstc=223492548.4c3ace39cf33b2cb2eee1347db4c651b.1539054315149.1539075414812.1539087413742.4; __hssc=223492548.2.1539087413742',
            'referer': 'https://www.indiegogo.com/explore/all?project_type=campaign&project_timing=all&sort=trending',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        self.flag = True

    def get_post_data(self, page_num):
        data = '''{
            "sort": "trending",
            "category_main": null,
            "category_top_level": null,
            "project_timing": "all",
            "project_type": "campaign",
            "page_num": %d,
            "per_page": 12,
            "q": "",
            "tags": []
        }''' % page_num
        return data

    def get_response(self, url, post_data):
        response = requests.post(url, data=post_data, headers=self.headers)
        return response.content.decode()

    def parse_response(self, resp_str):
        resp_json = json.loads(resp_str)
        resp_list = resp_json["response"]["discoverables"]
        ret_list = []
        for li_dict in resp_list:
            # 1.提取原始列表中所需要的字段
            data_dict = {
                "project_id": li_dict["project_id"],
                "project_type": li_dict["project_type"],
                "title": li_dict["title"],
                "tagline": li_dict["tagline"],
                "clickthrough_url": li_dict["clickthrough_url"],
                "category": li_dict["category"],
                "currency": li_dict["currency"],
                "funds_raised_amount": li_dict["funds_raised_amount"],
                "funds_raised_percent": li_dict["funds_raised_percent"],
                "close_date": li_dict["close_date"],
            }
            # 2.1补充字段: 处理详情页数据(OVERVIEW)并加入列表
            data_dict = self.get_overview_data(data_dict)

            # 2.2补充字段: 处理详情页数据(STORY)并加入列表
            data_dict = self.get_story_data(data_dict)

            # 2.2补充字段: 处理时间数据并加入列表
            data_dict = self.deal_time(data_dict)

            ret_list.append(data_dict)

        return ret_list

    def deal_time(self, data_dict):
        try:
            # 处理时间数据并加入列表 li_dict["close_date"] -> "2018-10-17T23:59:59-07:00"
            # 获取当前日期
            now_datetime = datetime.datetime.now()
            temp_now_time = now_datetime.strftime('%Y-%m-%d %H:%M:%S')
            now_time = datetime.datetime.strptime(temp_now_time, '%Y-%m-%d %H:%M:%S')
            # 项目结束时的日期
            time_str = re.findall(r'(\d{4}-\d+-\d+T\d+:\d+:\d+)-.*?:.*?', data_dict["close_date"])[0] or temp_now_time
            project_time = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
            # project_time = datetime.datetime.strptime(
            # data_dict["close_date"].split('T')[0] + ' ' + data_dict["close_date"].split('T')[1].split('-')[0],
            # '%Y-%m-%d %H:%M:%S')
            # 间隔天数
            days = (project_time - now_time).days
            data_dict['days_left'] = days
        except Exception as e:
            print('剩余时间字段处理异常: %s' % e)
            data_dict['days_left'] = 'error'
        return data_dict

    def get_overview_data(self, data_dict):
        try:
            url = 'https://www.indiegogo.com' + data_dict["clickthrough_url"]
            headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
            }
            resp = requests.get(url, headers=headers)
            html = resp.content.decode()
            ret = re.findall(r'"forever_funding_ends_at":.*?,"overview":"(.*?)","overview_image_url"', html, re.S)[0]
            data_dict['OVERVIEW'] = ret
        except Exception as e:
            print('获取overview失败: %s' % e)
            data_dict['OVERVIEW'] = ''
        return data_dict

    def get_story_data(self, data_dict):
        # https://www.indiegogo.com/private_api/campaigns/2417262/description
        try:
            url = 'https://www.indiegogo.com/private_api/' + data_dict['project_type'] + 's/' + str(
                data_dict['project_id']) + '/description'
            # print(url)  # 太骚了,这里url资源路径是复数,不过确实符合 RESTFUL 风格
            headers = {
                'accept': 'application/json, text/plain, */*',
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
            }
            resp = requests.get(url, headers=headers)
            resp_json = resp.content.decode('utf-8')
            resp_dict = json.loads(resp_json)

            # 进行xpath提取
            # print(resp_dict['response']['description_html'])
            html = etree.HTML(resp_dict['response']['description_html'])
            ret_list = html.xpath('(//p | //h2 | //h3)//text()')
            # print(ret_list)
            temp_list = []
            # temp_list = [' '.join(char.split()) for char in ret_list if char=="\xa0"]
            for char in ret_list:
                if char == "\xa0":
                    char = ''
                else:
                    char = char.replace('\xa0', ' ')
                temp_list.append(char)
            # print(temp_list)
            data_dict['STORY'] = ' '.join(temp_list) if len(temp_list) > 0 else ''
        except Exception as e:
            print('获取story失败: %s' % e)
            data_dict['STORY'] = ''
        return data_dict

    def save_data(self, data_dict):
        """数据保存"""
        with open('data.csv', 'a', encoding='utf-8') as csvfile:
            fieldnames = ["project_id", "project_type", "category", "title", 'tagline', "currency",
                          "funds_raised_amount", "funds_raised_percent", "close_date", 'days_left', 'OVERVIEW', 'STORY',
                          "clickthrough_url"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.flag:
                writer.writeheader()
                self.flag = False
            writer.writerow(data_dict)
        print('保存成功')

    def run(self):
        '''主程序'''
        # 1.url
        # 2.发送请求,获取响应
        page_num = 0
        while True:
            page_num += 1
            post_data = self.get_post_data(page_num)
            print('获取post_data成功', page_num)

            resp_str = self.get_response(self.url, post_data)
            if resp_str is None:
                continue
            print('获取resp_str成功', page_num)

            # 3.提取数据
            data_list = self.parse_response(resp_str)
            print('获取data_list成功', page_num)
            # 4.保存数据
            if len(data_list) == 12:
                for data_dict in data_list:
                    self.save_data(data_dict)
            elif len(data_list) < 12:  # per_page
                for data_dict in data_list:
                    self.save_data(data_dict)
                break
            else:
                break


if __name__ == '__main__':
    indiegogo_spider = IndiegogoSpider()
    indiegogo_spider.run()
