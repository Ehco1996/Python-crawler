'''
爬取一号店商品信息
'''

import requests
from bs4 import BeautifulSoup


def get_html_text(url):
    '''
    返回网页text
    '''
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        raise ValueError('errors')


def parse_good_detail(pmId, provinceId=5, cityid=37):
    '''
    查询指定id商品的库存和价格
    默认查询 江苏省 南京市 的库存
    '''
    # 一号点的Ajax服务器请求地址
    # 默认使用江苏省为省份信息
    url = 'http://gps.yhd.com/restful/detail?mcsite=1&provinceId={}&cityId={}&pmId={}&ruleType=2&businessTagId=16'.format(
        provinceId, cityid, pmId)
    text = get_html_text(url)
    # 对信息进行初步格式化 删掉data无用信息
    content = text[text.find('{') + 1:-2]
    data_dict = {}
    # 将所有的类json数据格式化存入字典
    for rec in content.split(','):
        data_dict[rec.split(":")[0].replace(
            '"', '').replace('"', '')] = rec.split(':')[1]

    # 查找我们想要的信息
    price = data_dict['currentPrice']
    stock = data_dict['currentStockNum']

    return price, stock


def parse_goods_info(url,provinceId=5, cityid=37):
    '''
    抓取指定url的所有商品的

    商品id
    价格
    库存
    链接

    returen: goods_infolist<dict in list>
    '''

    goods_infolist = []

    html = get_html_text(url)
    soup = BeautifulSoup(html, 'lxml')
    goods_list = soup.find_all('a', class_='mainTitle')

    for good in goods_list:
        url = good['href'][2:]
        title = ''.join(good['title'].split(' ')[:3])  # 对标题稍微格式化一下
        pmId = good['pmid']
        try:
            price, stock = parse_good_detail(pmId,provinceId,cityid)
        except:
            price, stock = '信息错误', '信息错误'

        goods_infolist.append(
            {'name': title, 'price': price, 'stock': stock, 'url': url})

    return goods_infolist


'''
# 一号店自营所有小米手机的商品筛选列表
xiaomi_url = 'http://list.yhd.com/c23586-0-81436/b969871-3923/?tc=3.0.10.3923.3&tp=52.23586.107.0.3.LsvLUR1-10-1FRQ7&ti=G78XlK'
# 测试抓取小米手机的信息
xiaomiPhone = parse_goods_info(xiaomi_url)
# 格式化输出一下
for rec in xiaomiPhone:
    print('型号: {}\t价格: {}\t库存: {}\t地址: {}'.format(
        rec['name'], rec['price'], rec['stock'], rec['url']))
'''
