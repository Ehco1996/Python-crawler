'''
爬取豆瓣电影 Top250

'''


import json
import os

import requests
from bs4 import BeautifulSoup

from panspider import parse_link


class Model():
    '''基类用来显示信息'''

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n {}>'.format(name, '\n '.join(properties))
        return s


class Movie(Model):
    '''存储电影信息的类
       存储了电影的 名字、分数、短语、封面图片、排名
    '''

    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0
        self.download_link = ''


def cached_url(url):
    '''缓存下载过的页面'''
    folder = 'cached_douban'
    # 通过url来定义文件名
    # url： https://movie.douban.com/top250?start=25
    filename = url.split('=')[-1] + '.html'
    # 关联目录和文件名生成绝对路劲
    path = os.path.join(folder, filename)

    # 当该文件被下载过了，直接从内存读取文件并返回
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedir(folder)
        # 发送网络请求，把结果/二进制写入文件
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)

        return r.content


def movie_form_div(div):
    '''从div中解析出电影的信息'''

    # 实例化电影对象
    m = Movie()
    m.name = div.find('div', class_='hd').text.strip().replace('\n', '')
    m.score = div.find('span', class_='rating_num').text
    m.cover_url = div.find('img')['src']
    m.ranking = div.find('em').text
    # 搜索下载链接
    name = m.name.strip().split('/')[0]
    m.download_link = parse_link(name)
    # 有的电影没有短语，特殊处理
    try:
        m.quote = div.find('span', class_='inq').text
    except:
        m.quote = '暂无短语'
    return m


def movies_from_url(url):
    '''从url中解析出所有电影'''

    page = cached_url(url)
    soup = BeautifulSoup(page, 'lxml')
    divs = soup.find_all('div', class_='item')
    movies = [movie_form_div(i) for i in divs]
    return movies


def save_to_file(movies):
    '''将结果写入文件'''
    filename = 'beautifulTop250.json'
    jsondata = {}
    jsondata['movies'] = []
    for movie in movies:
        # 保留第一个电影名版豆瓣电影250.xls
        content = dict(rank=movie.ranking, name=movie.name.strip().split('/')[0], score=movie.score,
                       quote=movie.quote, download_link=movie.download_link)
        '''
        原版
        content = dict(rank=movie.ranking, name=movie.name, score=movie.score,
                       quote=movie.quote, cover_url=movie.cover_url, download_link=movie.download_link)
        '''
        jsondata['movies'].append(content)

    with open(filename, 'a') as f:
        json.dump(jsondata, f, ensure_ascii=False)


def main():
    movies = []
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies += movies_from_url(url)
    save_to_file(movies)


if __name__ == '__main__':
    main()
