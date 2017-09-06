'''
Google Image Spider

'''

import requests
from bs4 import BeautifulSoup


SEARCHRUL = 'https://www.google.com/search?&safe=off&q={}&tbm=isch&tbs=itp:photo,isz:l'


def get_html_text(url):
    '''获取网页的原始text'''
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    try:
        r = requests.get(url, timeout=9, headers=headers)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def parse_img_url(q, nums):
    '''
    解析返回搜索图片的原始链接
    q ： 搜索关键词
    nums： 返回的结果数量 最大值20
    '''
    links = []
    # 防止越界
    if nums > 20 or nums > 0:
        num = 20

    url = SEARCHRUL.format(q)
    print(url)
    html = get_html_text(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find_all('div', class_='rg_meta', limit=nums)
        for link in content:
            rec = eval(link.text)
            links.append(rec['ou'])
        return links
    else:
        return 'error'


res = parse_img_url('test', 15)

for url in res:
    print(url)
