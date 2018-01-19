from toapi import Item, XPath


class Search(Item):
    __base_url__ = 'https://91baby.mama.cn/search.php?searchsubmit=yes'
    title = XPath('//li[@class="pbw"]/h3/text()')

    class Meta:
        source = XPath('//div[@class="slst mtw"]')
        route = {'/hotbook?page=:page': '/forum-171-:page.html'}

    def clean_book_id(self, book_id):
        return book_id.split('-')[1]
