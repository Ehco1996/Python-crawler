# -*- coding: utf-8 -*-

'''
Time 2017-11-18
Author Ehco1996

爬取搜狗词库
'''

import os
import sys
import time

import requests
from bs4 import BeautifulSoup


# 设置项目路径，方便我们导包
PROJECT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'sougou'))

from store_new.stroe import DbToMysql
from utils.tools import UtilLogger
import configs


def get_html_text(url):
    try:
        r = requests.get(url, timeout=15, stream=True)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return -1


class Sougou_spider():
    '''
    搜狗词库爬虫
    '''

    def __init__(self):
        self.store = DbToMysql(configs.TEST_DB)
        self.log = UtilLogger('SougouSpider',
                              os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_SougouSpider.log'))

    def cate_ext(self, html, type1):
        '''
        解析列表页的所有分类名
        Args:
            html 文本
            type1 一级目录名        
        '''
        res = []
        soup = BeautifulSoup(html, 'lxml')
        cate_list = soup.find('div', {'id': 'dict_cate_show'})
        lis = cate_list.find_all('a')
        for li in lis:
            type2 = li.text.replace('"', '')
            url = 'http://pinyin.sogou.com' + li['href'] + '/default/{}'
            res.append({
                'url': url,
                'type1': type1,
                'type2': type2,
            })
        return res

    def list_ext(self, html, type1, type2):
        '''
        解析搜狗词库的列表页面
        args：
            html： 文本
            type1 一级目录名 
            type2 二级目录名 
        retrun list
        每一条数据都为字典类型
        '''
        res = []
        try:
            soup = BeautifulSoup(html, 'lxml')
            # 偶数部分
            divs = soup.find_all("div", class_='dict_detail_block')
            for data in divs:
                name = data.find('div', class_='detail_title').a.text
                url = data.find('div', class_='dict_dl_btn').a['href']
                res.append({'filename': type1 + '_' + type2 + '_' + name,
                            'type1': type1,
                            'type2': type2,
                            'url': url,
                            })
            # 奇数部分
            divs_odd = soup.find_all("div", class_='dict_detail_block odd')
            for data in divs_odd:
                name = data.find('div', class_='detail_title').a.text
                url = data.find('div', class_='dict_dl_btn').a['href']
                res.append({'filename': type1 + '_' + type2 + '_' + name,
                            'type1': type1,
                            'type2': type2,
                            'url': url,
                            })
        except:
            print('解析失败')
            return - 1
        return res

    def start(self):
        '''
        解析搜狗词库的下载地址和分类名称
        '''
        cate_list = self.store.find_all('sougou_cate')
        for cate in cate_list:
            type1 = cate['type1']
            type2 = cate['type2']
            for i in range(1, int(cate['page']) + 1):
                print('正在解析{}的第{}页'.format(type1 + type2, i))
                url = cate['url'].format(i)
                html = get_html_text(url)
                if html != -1:
                    res = self.list_ext(html, type1, type2)
                    self.log.info('正在解析页面 {}'.format(url))
                    for data in res:
                        self.store.save_one_data('sougou_detail', data)
                        self.log.info('正在存储数据{}'.format(data['filename']))
                time.sleep(3)


class Download_scel():
    '''
    词库文件下载
    '''

    def __init__(self):
        self.store = DbToMysql(configs.TEST_DB)
        self.log = UtilLogger('SougouDownloader',
                              os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_SougouDownloader.log'))

    def get_html_content(self, url):
        '''
        从url下载对应的二进制文件
        '''
        try:
            r = requests.get(url, timeout=30, stream=True)
            r.raise_for_status
            return r.content
        except:
            return -1

    def download_file(self, content, filename):
        '''
        下载搜狗词库
        保存scel文件
        '''
        path = os.path.join("/Users/ehco/Desktop/input/", filename)
        with open(path + '.scel', 'wb') as f:
            f.write(content)
            print('{}词库文件保存完毕'.format(filename))

    def strip_wd(self, s):
        '''
        去除字符串中的非法字符
        '''
        kwd = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
               '(', ')', '.', '/', '|', '>', '<', '\\', '*', '"', '“', ]
        ans = ''
        for i in s:
            if i not in kwd:
                ans += i
        return ans

    def start(self):
        # 从数据库检索记录
        res = self.store.find_all('sougou_detail')
        self.log.warn('一共有{}条词库等待下载'.format(len(res)))
        for data in res:
            content = self.get_html_content(data['url'])
            filename = self.strip_wd(data['filename'])
            # 如果下载失败，我们等三秒再重试
            if content == -1:
                time.sleep(3)
                self.log.info('{}下载失败 正在重试'.format(filename))
                content = self.get_html_content(data[1])
            self.download_file(content, filename)
            self.log.info('正在下载文件{}'.format(filename))
            time.sleep(1)


# if __name__ == '__main__':
#     #Sougou_spider().start()
#     #Download_scel().start()
