'''
解析91baby 新书热书列表页
'''

from collections import OrderedDict
from toapi import Item, XPath


class MyItem(Item):
    @classmethod
    def parse(cls, html):
        """Parse html to json"""
        if cls.Meta.source is None:
            return cls._parse_item(html)
        else:
            sections = cls.Meta.source.parse(html, is_source=True)
            results = []
            for section in sections:
                res = cls._parse_item(section)
                if res:
                    results.append(res)
            return results

    @classmethod
    def _parse_item(cls, html):
        item = OrderedDict()
        for name, selector in cls.__selectors__.items():
            try:
                item[name] = selector.parse(html)
            except Exception:
                item[name] = ''
            clean_method = getattr(cls, 'clean_%s' % name, None)
            if clean_method is not None:
                res = clean_method(cls, item[name])
                if res == None:
                    return None
                else:
                    item[name] = res
        return item


class HotBook(MyItem):
    __base_url__ = 'http://91baby.mama.cn'
    title = XPath('//a[@class="xst"]/text()[1]')
    author = XPath('//a[@class="xst"]/text()[1]')
    url = XPath('//a[@class="xst"]/@href')
    book_id = XPath('//a[@class="xst"]/@href')

    def clean_title(self, title):
        if '《' in title:
            return title[title.find('\u300a') + 1:title.find('\u300b')][:10]
        else:
            return None

    def clean_author(self, author):
        if ':' in author:
            return author[author.find(':') + 1:author.find('(')]
        elif '：' in author:
            return author[author.find('：') + 1:author.find('（')]
        else:
            return None

    def clean_book_id(self, book_id):
        return book_id.split('-')[1]

    class Meta:
        source = XPath('//tbody[@class="thread_tbody"]')
        route = {'/hotbook?page=:page': '/forum-171-:page.html'}
