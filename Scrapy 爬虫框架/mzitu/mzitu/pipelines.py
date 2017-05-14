# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests

class MzituPipeline(object):
    def process_item(self, item, spider):
        
        base_dir = '/Users/ehco/Desktop/mezitu/'
        # 防止目录不存在！
        if not os.path.exists(base_dir+item['name']):
            os.makedirs(base_dir+item['name'])
        
        # 生成图片下载列表：
        url_list = item['img_urls']
        for i in range(len(url_list)):
            open(base_dir+item['name']+'/'+str(i),'wb').write(requests.get(url_list[i]).content)        
        return item
