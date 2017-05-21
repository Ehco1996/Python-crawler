# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 小说名字
    bookname = scrapy.Field()
    #章节名
    title = scrapy.Field()
    #正文
    body  = scrapy.Field()
    #排序用id
    order_id = scrapy.Field()