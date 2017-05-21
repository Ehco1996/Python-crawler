# -*- coding: utf-8 -*-
import scrapy
from biquge.items import BiqugeItem
from .sjzh import Cn2An,get_tit_num


class XsphspiderSpider(scrapy.Spider):
    name = "xsphspider"
    allowed_domains = ["qu.la"]
    start_urls = ['http://www.qu.la/paihangbang/']
    novel_list = []

    def parse(self, response):

        # 找到各类小说排行榜名单
        books = response.xpath('.//div[@class="index_toplist mright mbottom"]')

        # 找到每一类小说排行榜的每一本小说的下载链接
        for book in books:
            links = book.xpath('.//div[2]/div[2]/ul/li')
            for link in links:
                url = 'http://www.qu.la' + \
                    link.xpath('.//a/@href').extract()[0]
                self.novel_list.append(url)

        # 简单的去重
        self.novel_list = list(set(self.novel_list))

        for novel in self.novel_list:
           yield scrapy.Request(novel, callback=self.get_page_url)

    def get_page_url(self, response):
        '''
        找到章节链接
        '''
        page_urls = response.xpath('.//dd/a/@href').extract()

        for url in page_urls:
           yield scrapy.Request('http://www.qu.la' + url,callback=self.get_text)

    def get_text(self, response):
        '''
        找到每一章小说的标题和正文
        并自动生成id字段，用于表的排序
        '''
        item = BiqugeItem()

        # 小说名
        item['bookname'] = response.xpath(
            './/div[@class="con_top"]/a[2]/text()').extract()[0]
        
        # 章节名 ,将title单独找出来，为了提取章节中的数字
        title = response.xpath('.//h1/text()').extract()[0]
        item['title'] = title
        
        #  找到用于排序的id值
        item['order_id'] = Cn2An(get_tit_num(title))
        
        # 正文部分需要特殊处理
        body = response.xpath('.//div[@id="content"]/text()').extract()
        
        # 将抓到的body转换成字符串，接着去掉\t之类的排版符号，
        text = ''.join(body).strip().replace('\u3000', '')
        
        item['body'] = text

        return item
