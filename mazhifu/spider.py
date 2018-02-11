import os
import time
from datetime import datetime, timedelta

import requests
from lazyspider.lazystore import LazyMysql
from selenium import webdriver

from config import TEST_DB, USERNMAE, PASSWD
# 在当前目录运创建data目录
CSV_DIR = os.path.abspath(os.curdir) + '/csvdata/'
if not os.path.isdir(CSV_DIR):
    os.mkdir(CSV_DIR)


class Mazhifu(object):
    '''获取码支付cookies'''

    def __init__(self, headers, user, passwd):
        '''
        类的初始化

        headers：请求头
        cookies: 持久化访问
        info_list: 存储账单信息的列表
        '''
        self.headers = headers
        # 初始化用户名和密码
        self.user = user
        self.passwd = passwd

    def wait_input(self, ele, str):
        '''减慢账号密码的输入速度'''
        for i in str:
            ele.send_keys(i)
            time.sleep(0.2)

    def get_cookies(self):
        '''获取cookies'''

        # 初始化浏览器对象
        sel = webdriver.PhantomJS()
        # sel = webdriver.Chrome()
        sel.get('https://codepay.fateqq.com/login.html')
        sel.implicitly_wait(3)
        # 找到用户名字输入框
        uname = sel.find_element_by_name('username')
        uname.clear()
        print('正在输入账号.....')
        self.wait_input(uname, self.user)
        time.sleep(1)
        # 找到密码输入框
        upass = sel.find_element_by_name('password')
        upass.clear()
        print('正在输入密码....')
        self.wait_input(upass, self.passwd)
        # 截图查看
        # sel.save_screenshot('1.png')
        # 找到登录按钮
        butten = sel.find_element_by_xpath(
            '//*[@id="login-form"]/footer/button')
        time.sleep(1)
        butten.click()
        # sel.save_screenshot('2.png')
        print(sel.current_url)
        # 跳转到账单页面
        print('正在跳转页面....')
        sel.implicitly_wait(3)
        # sel.save_screenshot('3.png')
        # 获取cookies 并转换为字典类型
        cookies = sel.get_cookies()
        cookies_dict = {}
        for cookie in cookies:
            if 'name' in cookie and 'value' in cookie:
                cookies_dict[cookie['name']] = cookie['value']
        # 关闭浏览器
        sel.close()
        print(cookies_dict)
        return cookies_dict


def download_csv_by_date(date, cookies, headers):
    '''
    下载指定日期的账单csv
    date<str> 2018-01-19
    cookies&headers<dict>
    '''
    csv_url = 'https://codepay.fateqq.com/order.html?csv=1&type=0&status=NaN&startdate={}&finishdate={}&pay_id='.format(
        date, date)
    r = requests.get(csv_url, cookies=cookies, headers=headers, verify=False)

    try:
        with open(CSV_DIR+'/{}.csv'.format(date), 'w') as f:
            f.write(r.content.decode('GB2312'))
        print('日期：{} 账单下载成功'.format(date))
    except:
        print('error！  日期：{} 账单下载失败！！！'.format(date))


def deal_csv_file(filename):
    '''
    读取csv文件，解析出必要的信息
    返回一个列表items
    每个item是一个存放张当信息的dict
    '''
    with open(filename, 'r') as f:
        items = []
        lines = f.readlines()
        # 去掉第一行头信信息
        for line in lines[1:]:
            data = line.split(',')
            date = data[0]
            way = data[2]
            if len(way) == 0:
                way = 'QQ支付'
            try:
                username = data[3].split('@')[1]
                user_id = data[3].split('@')[0]
            except:
                username = '用户名不合法'
                user_id = '-1'
            trade_no = data[4]
            raw_price = data[5]
            pay_price = data[6]
            status = data[7]
            if status == '支付失败':
                cash = -1
            else:
                cash = 0
            item = {
                'date': date,  # 日期
                'way': way,   # 支付方式
                'username': username,  # 用户名
                'trade_no': trade_no,  # 订单号
                'raw_price': raw_price,  # 申请价格
                'pay_price': pay_price,  # 支付价格
                'status': status,  # 支付状态
                'user_id': user_id,  # 91pay id
                'cash': cash
            }
            items.append(item)
    return items


def main():
    # 自定义headers
    HEADERS = {'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,mt;q=0.7',
               'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_13_2)AppleWebKit/537.36(KHTML,likeGecko)Chrome/63.0.3239.132Safari/537.36', 'Accept': 'text/html,*/*;q=0.01', 'Referer': 'https', 'X-Requested-With': 'XMLHttpRequest', 'If-None-Match': 'W/"urgS8taZT5JSp1x4JyJV0g=="', 'Connection': 'keep-alive--compressed'}

    # 模拟登录获取cookies:
    pay = Mazhifu(HEADERS, USERNMAE, PASSWD)
    COOKIES = pay.get_cookies()
    # 昨天日期
    yesterday = (datetime.today()-timedelta(days=1)) .strftime('%Y-%m-%d')
    # 下载今日的账单文件
    download_csv_by_date(yesterday, COOKIES, HEADERS)
    # 处理csv文件并入库
    items = deal_csv_file(CSV_DIR+yesterday + '.csv')
    # 建立数据库链接
    store = LazyMysql(TEST_DB)
    for item in items:
        # 数据根据日期和方式去重
        res = store.find_by_fields(
            'cmf_pay_orders', {'date': item['date'], 'way': item['way']})
        if len(res) == 0:
            store.save_one_data(item, 'cmf_pay_orders')


if __name__ == "__main__":
    main()
