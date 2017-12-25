'''
下载FC吧公用网盘中的nes游戏资源
地址： http://fcnes.ys168.com/
'''


import requests
from bs4 import BeautifulSoup
from lazyspider.lazyheaders import LazyHeaders
import os

# 静态文件目录
DOWNLOADPATH = '/Users/ehco/Desktop/FCBA/'

# 获取cookies 和headers
raw_curl = "curl 'http://fcnes.ys168.com/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,mt;q=0.7' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: ASP.NET_SessionId=4hczdrmla3vjnektrww4lnov' -H 'Connection: keep-alive' --compressed"
lz = LazyHeaders(raw_curl)
COOKIES = lz.getCookies()
HEADERS = lz.getHeaders()


def get_html_response(url):
    try:
        r = requests.get(url, headers=HEADERS, cookies=COOKIES)
        r.raise_for_status
        return r.content
    except:
        return -1


with open(DOWNLOADPATH + 'fc.html') as f:
    html = f.read()


def ext_dowdload_url(html):
    res = {}
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find_all('li', class_='zml')
    for li in lis:
        dir_name = li.find('a').text
        res[dir_name] = []
        games = li.find_all("li", class_='xwj')
        for a in games:
            game = a.find('a')
            file_name = game.text
            url = game['href']
            res[dir_name].append((file_name, url))
    return res


res = ext_dowdload_url(html)

for k, v in res.items():
    dir_name = k
    for game in v:
        file_name = game[0]
        url = game[1]
        path = DOWNLOADPATH + dir_name
        try:
            os.mkdir(path)
        except:
            path
        with open(path + '/' + file_name, 'wb+') as f:
            f.write(get_html_response(url))
