# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProxyPipeline(object):
    '''
    这里我们通过对spider name的判断
    来分清楚item是哪一个spider传来的
    从而做出不同的处理方式
    '''
    
    def process_item(self, item, spider):
        if spider.name == 'dxdlspider':
            content = item['addr'].split('\r\n')
            for line in content:
                open('/Users/ehco/Desktop/result/dx_proxy.txt','a').write(line+'\n')


        elif spider.name=='kdlspider':
            #我们直接将传来的addr写入文本
            open('/Users/ehco/Desktop/result/kdl_proxy.txt','a').write(item['addr']+'\n')

        return item
