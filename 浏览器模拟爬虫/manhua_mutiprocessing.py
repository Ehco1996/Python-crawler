'''
理由Selenium库爬取漫画网站
并将漫画保存到本地
爬取的地址是：http://comic.sfacg.com/
多线程版本，没有解决ip封锁的问题
'''

import os
from selenium import webdriver
import requests
from multiprocessing.dummy import Pool as ThreadPool


class Item():
    '''
    模拟Scrapy
    创建一个类
    保存漫画的章节名和url地址
    '''
    url = None
    name = None


def mkdir(path):
    '''
    防止目录存在
    '''
    if not os.path.exists(path):
        os.mkdir(path)


def SavePic(item):
    '''
    通过requests库
    将抓取到的图片保存到本地
    '''
    url = item.url
    filename = item.name
    content = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(content)
    print('当前文件 {} 下载完毕'.format(filename))

def get_TOF(index_url):
    '''
    获取漫画的目录中的每一章节的url连接
    并返回一个字典类型k：漫画名 v：章节链接
    '''
    url_list = []

    # 模拟浏览器并打开网页
    browser = webdriver.PhantomJS()
    browser.get(index_url)
    browser.implicitly_wait(3)

    # 找到漫画标题 并创建目录
    title = browser.title.split(',')[0]
    mkdir(title)

    # 找到漫画章节，注意，漫画可能会有多种篇章
    # 例如番外，正文，短片等等
    comics_lists = browser.find_elements_by_class_name('comic_Serial_list')

    # 寻找、正文等
    for part in comics_lists:
        # 找到包裹链接的links
        links = part.find_elements_by_tag_name('a')
        # 找到每个单独的章节链接
        for link in links:
            url_list.append(link.get_attribute('href'))

    # 关闭浏览器
    browser.quit()

    Comics = dict(name=title, urls=url_list)

    return Comics


def get_pic(Comics):
    '''
    打开每个章节的url，
    找到漫画图片的地址，
    保存在列表并返回
    '''
    # 用于保存item的列表
    comics_urls = []

    # 从dict里分离漫画名和章节链接
    comic_list = Comics['urls']
    basedir = Comics['name']

    browser = webdriver.PhantomJS()
    for url in comic_list:
        browser.get(url)
        browser.implicitly_wait(3)

        # 创建章节目录
        dirname = basedir + '/' + browser.title.split('-')[1]
        mkdir(dirname)
        # 找到该漫画一共有多少页
        pageNum = len(browser.find_elements_by_tag_name('option'))

        # 找到下一页的按钮
        nextpage = browser.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
        # 找到图片地址，并点击下一页
        for i in range(pageNum):
            item = Item()
            item.url = browser.find_element_by_id(
                'curPic').get_attribute('src')
            item.name = dirname + '/' + str(i) + '.png'
            comics_urls.append(item)
            nextpage.click()
        browser.quit()

    return comics_urls


def main():

    Comics_index = get_TOF('http://manhua.sfacg.com/mh/TTQQXY/')
    Comics_items = get_pic(Comics_index)

    # 开启多线程 线程数10
    pool = ThreadPool(1)
    pool.map(SavePic,Comics_items)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
