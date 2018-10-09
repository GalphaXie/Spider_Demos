# -*- coding: utf-8 -*-
# @File : cookies_str_to_dict.py
# @Author : Xie
# @Desc   : 处理Cookie成键值对
from pprint import pprint

headers = {
    'Cookie': 'uuid_tt_dd=-5896434016198114006_20171119; ADHOC_MEMBERSHIP_CLIENT_ID1.0=50ac7452-0ff3-a256-f940-b4d223d190c4; __yadk_uid=4pV3e70j3fLfr9qEdF5gojUqcVa4bfFP; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=1788*1*PC_VC; kd_user_id=ab16aee2-4287-4940-8c6f-fc15666e9087; UN=DefaultTest; bdshare_firstime=1527560745355; smidV2=20180701232804f0acbaa0eb3f6c8a5d70c1ea05d9d65c00efdc38d65162670; __utma=17226283.846950398.1533599134.1533599134.1533599134.1; __utmz=17226283.1533599134.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; UM_distinctid=165f0d4354112d-032d02c9729287-9393265-e1000-165f0d43543f1; CNZZDATA1259587897=1724199607-1537341536-%7C1537341536; ARK_ID=JSdbbc72aa72c47c6c74e703cfd807832edbbc; dc_session_id=10_1538182145317.847605; UserName=DefaultTest; UserInfo=7F1MouSm5h2RHg1zon0p8dYEUMsSro%2BLuLvzNMVwGDQ%2Fe12QB8NjJrg5%2B1KR4C50ZxBkCRUfe7t7Mxg2dJLPBIAj4Bj78KZhH%2F1aHLNkUXXJS9cSU%2Bb4Vm%2Fxpp%2BJVbogqyipIXwgIkWDAG9b0T1wAg%3D%3D; UserNick=DefaultTest; AU=371; BT=1539005722959; UserToken=7F1MouSm5h2RHg1zon0p8dYEUMsSro%2BLuLvzNMVwGDQ%2Fe12QB8NjJrg5%2B1KR4C50ZxBkCRUfe7t7Mxg2dJLPBIAj4Bj78KZhH%2F1aHLNkUXXJS9cSU%2Bb4Vm%2Fxpp%2BJVbogSbNJhmcyefKYXP95XifQEI5%2F75YsBKmUkeN%2FCYOO8YGv7W%2BBEqBpO%2FrL1i9FwOBt; TY_SESSION_ID=14f255a6-43a5-4874-9262-960e0a0d6bb2; dc_tos=pgbyuj; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1539065833,1539069913,1539081836,1539086636; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1539086636'
}

# 类似列表推导式的字典推导式(注意:实际上这里提取的值还是单一值的方式,不是元祖)
temp_dict = {i.split('=')[0]: i.split('=')[1] for i in headers['Cookie'].split('; ')}
pprint(temp_dict)
