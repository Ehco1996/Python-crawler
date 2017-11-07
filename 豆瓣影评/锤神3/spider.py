'''
爬取豆瓣影评
雷神3的所有评价
并存入数据库
'''

import time
import os


import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie

from stroe import DbToMysql
import config

request_url = 'https://movie.douban.com/subject/25821634/comments?start={}&limit=20'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
}

COOKIES = '''
bid=i2jh3YGuvEo; ll="118163"; gr_user_id=f52deadb-5f46-491c-9b52-4294ab176b90; viewed="1430904_25806793_25901403"; ps=y; dbcl2="169273073:UOYgsqmzhSs"; ck=m7xV; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1509972471%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fsource%3Dsuggest%26q%3D%25E9%259B%25B7%25E7%25A5%259E3%22%5D; ct=y; _vwo_uuid_v2=4EE59BFD9BF5C48E3E9020C6DE3564D4|d2deb1b903e06e32351743192190c582; ap=1; _pk_id.100001.4cf6=0377929d7299aea4.1508405769.14.1509975906.1509934106.; _pk_ses.100001.4cf6=*; __utma=30149280.341450299.1508041022.1509932565.1509972306.17; __utmb=30149280.32.10.1509972306; __utmc=30149280; __utmz=30149280.1509972306.17.13.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.16927; __utma=223695111.1000856564.1508405769.1509932565.1509972471.14; __utmb=223695111.0.10.1509972471; __utmc=223695111; __utmz=223695111.1509972471.14.10.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; push_noty_num=0; push_doumail_num=0
'''


def format_cookie(text):
    '''将字符串转换为字典形式的cookies'''
    cookie = SimpleCookie(text)
    return {i.key: i.value for i in cookie.values()}


def get_html_text(url, header={}, cookies={}):
    '''
    下载网页数据
    返回文本文件
    '''
    try:
        # 使用Session来最会话管理
        s = requests.Session()
        s.headers.update(header)
        s.cookies.update(cookies)
        r = s.get(url)
        r.raise_for_status
        return r.content
    except:
        return -1


def parse_detail(html):
    '''解析影评内容'''
    results = []
    try:
        soup = BeautifulSoup(html, 'lxml')
        comments = soup.find_all('div', class_='comment-item')
        for comment in comments:
            info = comment.find('span', class_='comment-info')
            name = info.contents[1].get_text().strip()
            try:
                # 针对没有评星的情况特殊处理
                star = info.contents[5]['title']
                time = info.contents[7].get_text().strip()
            except:
                star = '暂无评分'
                time = info.contents[5].get_text().strip()
            vote = comment.find('span', class_='votes').text.strip()
            content = comment.find('p').get_text().strip()
            results.append({
                'name': name,  # 作者名
                'star': star,  # 推荐程度
                'time': time,  # 时间
                'vote': vote,  # 赞同数
                'content': content  # 影评内容
            })
        return results
    except:
        print('内容解析错误')
        return -1


def cached_url(url):
    '''将访问过的url缓存到本地'''
    folder = 'cached_url'
    filename = url.split('?')[1].split('&')[0].split('=')[1] + '.html'
    path = os.path.join(folder, filename)
    # 如果文件缓存过了，读文件并返回
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 建立文件夹用于保存网页
        if not os.path.exists(folder):
            os.mkdir(folder)
        html = get_html_text(url, HEADERS, format_cookie(COOKIES))
        if html != -1:
            with open(path, 'wb') as f:
                f.write(html)
            return html
        else:
            print('{}下载失败'.format(filename))
            return -1


def main():
    store = DbToMysql(config.EHCO_DB)
    for i in range(0, 20001, 20):
        html = cached_url(request_url.format(i))
        #time.sleep(3)
        if html != -1:
            res_list = parse_detail(html)
            if res_list != -1:
                for data in res_list:
                    store.save_one_data('GodOfHammer_1', data)
                print('第{}页保存完毕'.format(i))
    store.close()


if __name__ == '__main__':
    main()
