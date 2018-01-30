import json

from toapi import Api
import requests

from items.hotbook import HotBook
from items.book import Book
from items.search import Search
from settings import MySettings





api = Api('', settings=MySettings)
api.register(HotBook)
api.register(Book)
api.register(Search)


@api.server.app.route('/search/<keyword>')
def search_page(keyword):
    '''
    91bay新书论坛
    搜索功能
    '''
    data = {
        'searchsel': 'forum',
        'mod': 'forum',
        'srchtype': 'title',
        'srchtxt': keyword,
    }
    r = requests.post(
        'http://91baby.mama.cn/search.php?searchsubmit=yes', data)
    r.encoding = 'utf8'
    html = r.text
    results = {}
    items = [Search]
    # 通过toapi的方法对网页进行解析
    for item in items:
        parsed_item = api.parse_item(html, item)
        results[item.__name__] = parsed_item
    # 返回json
    return api.server.app.response_class(
        response=json.dumps(results, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    api.serve()
