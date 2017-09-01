'''
一号店商品信息查询

'''

# 导入城市省份资源文件
from citydict import CITY_MAP

# 导入爬虫程序
from spider import parse_goods_info
import time


def main():
    good = input('请输入需要查询的商品:\t')
    city = input('请输入查询城市:\t')
    provinceId = CITY_MAP[city]['provinceId']
    cityid = CITY_MAP[city]['cityid']
    searc_url = 'http://search.yhd.com/c0-0/k' + good

    print('正在搜索相关商品')
    res = parse_goods_info(searc_url, provinceId, cityid)
    print('搜索完毕.....正在处理数据')

    for rec in res:
        print('型号: {}\t价格: {}\t库存: {}\t地址: {}'.format(
            rec['name'], rec['price'], rec['stock'], rec['url']))
        time.sleep(0.5)


if __name__ == '__main__':
    main()
