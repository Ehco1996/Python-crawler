'''
解析1号店的所有
省份
城市信息
'''
import os
from bs4 import BeautifulSoup

# 获取当前运行目录
path = os.path.dirname(os.path.abspath(__file__))


with open(path + '/cityid.html') as f:
    html = f.read()


def get_cityid_map(html):
    '''
    解析一号店省份、城市id
    return <dict>
    '''
    cityid_map = {}
    soup = BeautifulSoup(html, 'lxml')
    # 找到所有的a标签
    citys = soup.find_all('a')
    # 开始解析城市名城市id 省份id
    for city in citys:
        name = city.text.replace('市','')
        provinceId = city['data-provinceid']
        cityid = city['data-cityid']
        cityid_map[name] = {'provinceId': provinceId, 'cityid': cityid, }

    return cityid_map


print(get_cityid_map(html))
