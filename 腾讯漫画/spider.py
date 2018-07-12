import re
import json
import base64
from urllib import parse

import requests
from requests_html import HTML
from requests.adapters import Retry
from requests.adapters import HTTPAdapter


class Spider:

    def __init__(self):
        self.session = requests.session()
        # add requests http adapter with retry, including
        http_adapter = HTTPAdapter(max_retries=Retry(
            total=3, method_whitelist=frozenset(['GET', 'POST', 'PUT'])))
        self.session.mount('http://', http_adapter)
        self.session.mount('https://', http_adapter)

    def update_session_headers(self, headers):
        self.session.headers.update(headers)

    def get_html(self, url):
        try:
            r = self.session.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('get html failed')
            return None

    def parser(self, text):
        '''文本转换为reques_html的对象，方便我们做各种解析'''
        return HTML(html=text)


class TxComic(Spider):

    COMIC_HOST = 'http://ac.qq.com'
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/65.0.3325.146 Safari/537.36')
    }

    def __init__(self, comic_id):
        '''
        init腾讯漫画的爬虫
        comic_id 是漫画的id 比如海贼王的是`505430`
        '''
        super(TxComic, self).__init__()
        self.comic_id = comic_id
        self.update_session_headers(TxComic.HEADERS)

    def save_to_json(self, name, info):
        with open(name, 'w') as f:
            json.dump(info, f, ensure_ascii=False)

    def get_chapter_info(self):
        '''获取漫画的章节地址'''
        chapter_info = {}
        url = 'http://ac.qq.com/Comic/ComicInfo/id/{}'.format(self.comic_id)
        html_text = self.get_html(url)
        html = self.parser(html_text)

        # 找到所有章节列表
        ol = html.find('ol')[0]
        chapters = ol.find('a')
        index = 0
        for chapter in chapters:
            title = chapter.attrs['title']
            link = parse.urljoin(TxComic.COMIC_HOST, chapter.attrs['href'])
            key = '第{}章'.format(index)
            chapter_info[key] = {'title': title, 'link': link}
            index += 1
        return chapter_info

    def get_chapter_pics(self, url):
        '''获取指定章节漫画图片地址'''
        html_text = self.get_html(url)
        html = self.parser(html_text)

        b64_data = html.search("var DATA        = '{}'")[0][1:]
        info_str = base64.b64decode(b64_data).decode('utf-8')
        pics = json.loads(info_str)['picture']
        for pic in pics:
            pic.pop('width')
            pic.pop('height')
        return pics

    def get_comic_info(self):
        '''抓取本漫画的所有章节，图片信息，并保存到json'''
        chapters = self.get_chapter_info()
        for k, v in chapters.items():
            url = v['link']
            pics = self.get_chapter_pics(url)
            print(k, "图片地址解析完毕")
            v['pics'] = pics
        filename = "{}.json".format(self.comic_id)
        self.save_to_json(filename, chapters)
        print('漫画id ：{} 抓取完毕！'.format(self.comic_id))

def get_chapter_pics(self, url):
    '''获取指定章节漫画图片地址'''
    html_text = self.get_html(url)
    html = self.parser(html_text)

    b64_data = html.search("var DATA        = '{}'")[0][1:]
    info_str = base64.b64decode(b64_data).decode('utf-8')
    pics = json.loads(info_str)['picture']
    for pic in pics:
        pic.pop('width')
        pic.pop('height')
    return pics
