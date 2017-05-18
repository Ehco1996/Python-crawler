'''
从本地文件proxy.py中
读取可以用的代理列表
并从中随机选择一个代理
供给spider使用
'''


from xiubai.middlewares.proxy import proxies
import random

class RandomProxy(object):
    def process_request(self,request,spider):
        # 从文件中随机选择一个代理
        proxy = random.choice(proxies)

        request.meta['proxy'] = 'http://{}'.format(proxy)