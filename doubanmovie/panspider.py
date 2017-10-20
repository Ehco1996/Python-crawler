'''
根据关键字搜索对应的百度云下载链接

搜索地址：http://pansou.com/
'''


import os
import json

import requests
from bs4 import BeautifulSoup

api_url = 'http://api.pansou.com/search_new.php'


def cached_json(keyword):
    '''缓存下载过的json数据'''
    folder = 'cached_pansou'
    filename = keyword + '.json'
    # 关联目录和文件名生成绝对路劲
    path = os.path.join(folder, filename)

    # 当该文件被下载过了，直接从内存读取文件并返回
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 发送网络请求，把结果/json写入文件
        data = {
            'q': keyword,
            'p': 1,
        }
        r = requests.post(api_url, data=data).json()
        with open(path, 'a') as f:
            json.dump(r, f, ensure_ascii=False)
        return r


def parse_link(name):
    '''解析对应的下载连接'''
    j = cached_json(name)
    link = j['list']['data'][0]['link']
    return link



