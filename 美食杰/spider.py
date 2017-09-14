'''
美食节 各地小吃爬虫
主页url:  http://www.meishij.net/
排行榜url： http://top.meishi.cc/lanmu.php?cid=78
'''

# 导入相关库
import requests
from bs4 import BeautifulSoup


# 排行榜入口url
Base_url = 'http://top.meishi.cc/lanmu.php?cid=3'


def get_html_text(url):
    '''获取html文本'''
    try:
        r = requests.get(Base_url, timeout=3)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def parse_city_id(url):
    '''解析对应的城市排行榜连接'''

    res = []
    html = get_html_text(url)
    # 做一个简单的判断
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # 定位到 全国各地特色小吃排行榜分类,<div>
        cityids = soup.find('div', class_='rank_content_top')
        for city in cityids.find_all('a'):
            res.append({'name': city.text, 'url': city['href']})
        return res
    else:
        print('error !!!!')


def parse_food_info(url):
    '''解析对应的美食信息'''

    html = get_html_text(url)

    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # 定位到具体排行榜的位置
        foods = soup.find('div', class_='rank_content_top10_wraper')
        # 开始解析信息
        for food in foods.find_all('li'):
            # 寻找 食品名、做法链接、图片链接
            content = food.find('a', class_='img')
            name = content['title']
            detial_url = content['href']
            img_url = content.img['src']
            print('正在解析美食：{}'.format(name))
            # 构造一个生成器，分别返回 食物名,做法链接,图片链接
            yield name, detial_url, img_url
    else:
        print('error !!!!')


def main():
    '''程序入口'''

    # 找到所有城市排行榜的url
    citys = parse_city_id(Base_url)
    # 解析各个城市的美食
    for city in citys:
        city_name = city['name']
        # 利用生成器 迭代访问元素
        for food_name, detial_url, img_url in parse_food_info(city['url']):
            # 保存数据
            # save_data()
            pass
