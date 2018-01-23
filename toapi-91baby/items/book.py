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
    total_page = XPath('//span[@class="pgt"]/div//a')
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

    def clean_total_page(self, total_page):
        try:
            for index, page in enumerate(total_page):
                num = page.xpath('./text()')[0]
                if num == '下一页':
                    i = int(index) - 1
                    break
            page = total_page[i].xpath('./text()')[0]
            if '...' in page:
                return int(page.replace('... ', ''))
            return int(page)
        except:
            return 1

    class Meta:
        source = None
        route = {'/book_id=:id?page=:page': '/thread-:id-:page-1.html'}
