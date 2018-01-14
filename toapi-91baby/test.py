'''测试api的使用'''


import requests
import json

list_url = 'http://127.0.0.1:5000/hotbook?page={}'
book_url = 'http://127.0.0.1:5000/book?id={}?page={}'


def get_json_response(url):
    r = requests.get(url)
    return r.json()


# 获取第一页的所有书籍信息
page_json = get_json_response(list_url.format(1))

# 打印第一页的信息
for book in page_json['HotBook']:
    print(book['title'])
    print(book['book_id'])
