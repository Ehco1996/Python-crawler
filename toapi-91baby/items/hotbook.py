'''
解析91baby 新书热书列表页
'''


from toapi import Item, XPath


class HotBook(Item):
    __base_url__ = 'http://91baby.mama.cn'
    title = XPath('//a[@class="xst"]/text()[1]')
    url = XPath('//a[@class="xst"]/@href')
    book_id = XPath('//a[@class="xst"]/@href')

    class Meta:
        source = XPath('//tbody[@class="thread_tbody"]')
        route = {'/hotbook?page=:page': '/forum-171-:page.html'}

    def clean_book_id(self, book_id):
        return book_id.split('-')[1]
