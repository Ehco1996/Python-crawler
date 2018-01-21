'''
解析91baby 小说内容页
'''

from toapi import Item, XPath


def strip(text):
    '''去除字符串里的空白字符'''
    blank_str = ['\u3000\u3000', '\xa0', '\r', '\n']
    for i in blank_str:
        text = text.replace(i, '')
    return text


class Book(Item):
    __base_url__ = 'http://91baby.mama.cn'

    title = XPath('//*[@id="wp"]/div[3]/text()[3]')
    author = XPath('//*[@id="wp"]/div[3]/text()[3]')
    page = XPath('//div[@class="pg"]/a[@class="last"]/text()')
    contents = XPath('//td[@class="t_f"]')
    def clean_title(self, title):
        return title.split('《')[1].split('》')[0]

    def clean_author(self, author):
        index = author.find('作者：') + 3
        return author[index:]

    def clean_contents(self, contents):
        text = []
        for item in contents:
            content = strip(item.xpath('string(.)'))
            if len(content) < 128:
                text.append('全书完结!!! 以下的内容是网友书评！')
            text.append(content)
        return text

    def clean_page(self, page):
        num = (len(page))
        print(page)
        if num == 0:
            return 1
        else:
            return int(page[0].replace('...', ''))

    class Meta:
        source = None
        route = {'/book?id=:id?page=:page': '/thread-:id-:page-1.html'}
