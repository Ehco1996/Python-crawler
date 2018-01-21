from toapi import Item, XPath


class Search(Item):
    '''
    从搜索的界面解析出
    书名 id 链接 简介
    '''
    title = XPath('//h3/a/text()')
    book_id = XPath('//h3/a/@href')
    url = XPath('//h3/a/@href')
    content = XPath('//p[2]/text()')

    def clean_title(self, title):
        return ''.join(title)

    def clean_book_id(self, book_id):
        return book_id.split('-')[1]

    def clean_url(self, url):
        return url[:url.find('?')]

    class Meta:
        source = XPath('//li[@class="pbw"]')
        # 这里的route留空，防止重复注册路由
        route = {}
