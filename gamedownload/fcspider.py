'''
下载FC吧公用网盘中的nes游戏资源
地址： http://fcnes.ys168.com/
'''

import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from lazyspider.lazyheaders import LazyHeaders
# 当前文件目录加入path
PROJECT_PATH = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'gamedownload')
sys.path.append(PROJECT_PATH)


# 获取cookies 和headers
raw_curl = "curl 'http://www.fcnes.ys168.com/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,mt;q=0.7' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: ASP.NET_SessionId=wtugbdpdxlsieksfdpyiz3gu' -H 'Connection: keep-alive' --compressed"
lz = LazyHeaders(raw_curl)
COOKIES = lz.getCookies()
HEADERS = lz.getHeaders()

# urlbase，参数分别是网盘名，和分类id
list_base_url = 'http://c1.ys168.com/f_ht/ajcx/ml.aspx?cz=ml_dq&_dlmc={}'
detail_base_url = 'http://c1.ys168.com/f_ht/ajcx/wj.aspx?cz=dq&mlbh={}&_dlmc={}'

# 游戏文件的下载目录
download_path = '/Users/ehco/Desktop/fc/'


def get_html_response(url):
    try:
        r = requests.get(url, headers=HEADERS, cookies=COOKIES)
        r.raise_for_status
        return r.content
    except:
        return -1


def get_cached_html(url):
    '''html文件缓存器'''
    # 这里将url的第二个参数作为缓存的文件名
    file_name = url.split('=')[-2] + '.html'
    path = os.path.join(PROJECT_PATH, 'cached/' + file_name)
    if os.path.exists(path):
        print('{} 已经缓存过了'.format(file_name))
        with open(path, 'r') as f:
            return f.read()
    else:
        print('正在缓存文件：' + file_name)
        html = get_html_response(url)
        with open(path, 'w+') as f:
            f.write(html.decode('utf8'))
        return html


def ext_class_page(html):
    '''解析出列表页的分类名和id'''
    res = {}
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find_all('li', class_='gml')
    for li in lis:
        class_id = li['id'].split('_')[-1]
        class_name = li.find('a').text.replace('.', '')
        res[class_name] = class_id
    return res


def ext_dowdload_url(html):
    '''解析出游戏名和url'''
    res = {}
    soup = BeautifulSoup(html, 'lxml')
    games = soup.find_all("li", class_='xwj')
    for a in games:
        game = a.find('a')
        file_name = game.text
        url = game['href']
        res[file_name] = url
    return res


def download_game(path, res):
    '''下载游戏文件'''
    for k, v in res.items():
        file_path = os.path.join(path, k)
        try:
            with open(file_path, 'wb+') as f:
                print('正在下载: {}'.format(k))
                f.write(get_html_response(v))
                #time.sleep(0.5)
        except:
            print('{} 发生意外啦！'.format(k))


def main():
    # 解析列表页的分类名和id
    fc_html = get_cached_html(list_base_url.format('fcnes'))
    list_res = ext_class_page(fc_html)

    # 生成对应的详情页的url
    url_map = {}
    for k, v in list_res.items():
        url_map[k] = detail_base_url.format(v, 'fcnes')

    # 下载文件逻辑
    for name, url in url_map.items():
        dir_path = os.path.join(download_path, name)
        if os.path.exists(dir_path):
            print('该系列已经下载过了')
        else:
            os.mkdir(dir_path)
            print('正在下载系列: {} \n '.format(name))
            # 解析出文件下载链接
            res = ext_dowdload_url(get_cached_html(url))
            download_game(dir_path, res)


if __name__ == '__main__':
    main()
