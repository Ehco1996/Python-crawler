# -*- coding: utf-8 -*-
import scrapy
from mzitu.items import MzituItem


class MezituSpider(scrapy.Spider):
    name = "mezitu"
    allowed_domains = ["mzitu.com"]
    start_urls = ['http://www.mzitu.com/']
    # 初始化保存套图url的列表
    img_urls = []

    def parse(self, response):
        item = MzituItem()

        # 找到首页的每个妹子图的li列表
        main = response.xpath('//ul[@id="pins"]/li')
        
        '''
        for li in main:
            # 找到每个妹子图包的baseurl
            mzurl = li.xpath('./a/@href').extract()[0]
            # 找到每个妹子图的名字，传回去做dirname
            name = li.xpath('.//img/@alt').extract()[0]
            item['name'] = name

            # 进入套图页面，抓取每一张图
            yield scrapy.Request(mzurl, callback=self.get_pic_url)
        '''
        li = main[0]
        # 找到每个妹子图包的baseurl
        mzurl = li.xpath('./a/@href').extract()[0]
        # 找到每个妹子图的名字，传回去做dirname
        name = li.xpath('.//img/@alt').extract()[0]
        item['name'] = name

        # 进入套图页面，抓取每一张图
        yield scrapy.Request(mzurl, callback=self.get_pic_url)




        item['img_urls'] = self.img_urls
        
        print(self.img_urls)
        print("**************************************")
        print(item)
        
        yield item

    def img_url(self, response):
        '''
        从page_url的response里
        找到图片的下载连接
        '''
        # 找到图片的下载地址，注意有可能一页有两张图
        
        pic = response.xpath('//div[@class="main-image"]//img/@src').extract()
        
        for url in pic:
            self.img_urls.append(url)
            
    def get_pic_url(self, response):
        '''
        找到套图的最大页码，并且生成每一页的url连接 page_url
        '''
        max_num = response.xpath(
            '//div[@class="pagenavi"]/a[last()-1]/span/text()').extract()[0]
        for i in range(2, int(max_num) + 1):
            page_url = response.url + '/' + str(i)
            # 这是一个生成器，用来回调img_url函数来抓套图的url链接
            yield scrapy.Request(page_url, callback=self.img_url)
