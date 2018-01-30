'''
解析91baby 小说内容页
'''

from toapi import Item, XPath


def strip(text):
    '''去除字符串里的空白字符'''
    blank_str = ['\u3000\u3000', '\xa0', '\r']
    for i in blank_str:
        text = text.replace(i, '')
    return text


def strip_list(l):
    '''
    删除列表中的短字符串
    '''
    new_l = []
    for ele in l:
        if len(ele) > 5 and '本帖最后由' not in ele:
            new_l.append(ele)
    return new_l


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
        chapters = {}
        for index, item in enumerate(contents):
            content = strip(item.xpath('string(.)'))
            # 去掉开头废话
            if '当前被收藏数' not in content:
                chapters[index] = content
        book_contents = {}
        for k, v in chapters.items():
            # 过滤超断行
            texts = strip_list(v.split('\n'))
            book_contents[k] = texts
        return book_contents

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
