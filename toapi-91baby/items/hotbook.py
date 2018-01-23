'''
解析91baby 新书热书列表页
'''


from toapi import Item, XPath


class HotBook(Item):
    __base_url__ = 'http://91baby.mama.cn'
    title = XPath('//a[@class="xst"]/text()[1]')
    author = XPath('//a[@class="xst"]/text()[1]')
    url = XPath('//a[@class="xst"]/@href')
    book_id = XPath('//a[@class="xst"]/@href')

    def clean_title(self, title):
        if '《' in title:
            return title[title.find('\u300a') + 1:title.find('\u300b')][:10]
        else:
            return '广告贴'

    def clean_author(self, author):
        if ':' in author:
            return author[author.find(':') + 1:author.find('(')]
        elif '：' in author:
            return author[author.find('：') + 1:author.find('（')]
        else:
            return '广告贴'

    def clean_book_id(self, book_id):
        return book_id.split('-')[1]

    class Meta:
        source = XPath('//tbody[@class="thread_tbody"]')
        route = {'/hotbook?page=:page': '/forum-171-:page.html'}
