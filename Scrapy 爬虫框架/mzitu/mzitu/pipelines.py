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
        open(base_dir+item['name']+'/'+item['img_urls'][-6:],'wb').write(requests.get(item['img_urls']).content)        
        return item
