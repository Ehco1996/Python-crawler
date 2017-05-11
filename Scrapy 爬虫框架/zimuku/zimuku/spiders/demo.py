# -*- coding: utf-8 -*-
import scrapy

# 将我们需要爬的项目引入进来
from zimuku.items import ZimukuItem

class DemoSpider(scrapy.Spider):
    
    #该爬虫的名字
    name = "demo"
    
    #规定爬虫爬取网页的域名   
    allowed_domains = ["zimuku.net"]
    
    #开始爬取的url链接
    start_urls = ['http://zimuku.net/']

    def parse(self, response):
        '''
        parse()函数接收Response参数，就是网页爬取后返回的数据
        用于处理响应，他负责解析爬取的内容
        生成解析结果的字典，并返回新的需要爬取的请求
        '''

        #由于是demo 我们不做完全的功能，
        #只要求爬取出第一个字幕的名字
        #xpath规则可以通过查看网页源文件得出
        name = response.xpath('//b/text()').extract()[1]

        #建立一个items字典，用于保存我们爬到的结果，并返回给pipline处理
        items = {}
        items['第一个']= name

        return items
