# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BiqugePipeline(object):
    def process_item(self, item, spider):

        with open('/Users/ehco/Desktop/novel/' + item['bookname'] + '.txt', 'a+') as f:
            f.write(item['title'] + '\n\n')
            f.write(item['body'] + '\n\n')
