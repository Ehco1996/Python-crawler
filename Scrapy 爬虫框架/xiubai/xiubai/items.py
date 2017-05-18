# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiubaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    author = scrapy.Field()
    body = scrapy.Field()
    funNum = scrapy.Field()
    comNum = scrapy.Field()
    