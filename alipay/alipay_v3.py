'''
尝试持久化cookies
'''

import random
import time
from http.cookies import SimpleCookie

import requests
from bs4 import BeautifulSoup

# 初始手动传进来的cookies
COOKIES = 'J'

# 自定义headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Referer': 'https://my.alipay.com/portal/i.htm?referer=https%3A%2F%2Fauth.alipay.com%2Flogin%2Findex.htm',
    'Host': 'my.alipay.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive'
}


# 支付宝界面跳转的随机列表
URL_LIST = [{'url': 'https://my.alipay.com/portal/i.htm',
             'host': 'my.alipay.com',
             'referer':'https://my.alipay.com/portal/i.htm'},
            #{'url': 'https://lab.alipay.com/consume/record/items.htm',
            # 'host': 'lab.alipay.com'},
            {'url': 'https://my.alipay.com/wealth/index.html',
             'host': 'my.alipay.com',
             'referer':'https://my.alipay.com/portal/i.htm'},
            #{'url': 'https://custweb.alipay.com/account/index.htm',
             #'host': 'custweb.alipay.com'},
            {'url': 'https://my.alipay.com/portal/account/safeguard.htm',
             'host': 'my.alipay.com',
             'referer':'https://my.alipay.com/portal/i.htm'},
            #{'url': 'https://app.alipay.com/container/web/index.htm',
             #'host': 'app.alipay.com'},
            #{'url': 'https://zht.alipay.com/asset/newIndex.htm',
            # 'host': 'zht.alipay.com'},
            #{'url': 'https://personalweb.alipay.com/portal/i.htm',
            # 'host': 'personalweb.alipay.com'},
            ]


def trans_cookie(cok):
    '''将字符串转换为字典形式的cookies'''
    cookie = SimpleCookie(cok)
    return {i.key: i.value for i in cookie.values()}


def get_data(s):
    '''爬取账单洗信息页面'''

    info_list = []
    url = 'https://consumeprod.alipay.com/record/standard.htm'
    s.headers.update({'Host': 'consumeprod.alipay.com'})
    html = s.get(url)
    print(html)
    soup = BeautifulSoup(html.text, 'lxml')
    # 抓取前五个交易记录
    trades = soup.find_all('tr', class_='J-item ')[:5]
    for trade in trades:
        # 分别找到账单的 时间 金额 以及流水号
        time = trade.find('p', class_='text-muted').text.strip()
        amount = trade.find(
            'span', class_='amount-pay').text.strip()
        code = trade.find(
            'a', class_='J-tradeNo-copy J-tradeNo')['title']
        info_list.append(
            dict(time=time, amount=amount, code=code))
    return info_list


def keep_alive(s, l):
    '''更新Sessions状态，保持心调'''
    # 随机获取一个url
    seed = random.choice(l)
    # 更新header
    s.headers.update({'Host': seed['host']})
    s.headers.update({'Referer': seed['referer']})    
    # 更新cookies
    cok = s.cookies.get_dict()
    s.cookies.update(cok)
    # 返回更新过的Sessions
    time.sleep(random.randint(45, 120))
    return s


def get_status(s):
    # 抓取页面
    s.headers.update({'Host': 'consumeprod.alipay.com'})
    html = s.get('https://consumeprod.alipay.com/record/standard.htm')
    # 判断是否存活
    status = html.status_code
    print(status)
    if status == 200:
        cok = s.cookies.get_dict()
        s.cookies.update(cok)
        return True
    else:
        return False


# 初始化Sessions
chrome = requests.Session()
chrome.headers = HEADERS
chrome.cookies.update(trans_cookie(COOKIES))

#print(get_data(chrome))

minutes = 0


while True:
    
    if get_status(chrome):
        time.sleep(random.randint(1,10))
        data = get_data(chrome)
        minutes += 1
        print('坚持了{}分钟\n数据：{}'.format(minutes, data))
        # 保持心跳
        chrome = keep_alive(chrome, URL_LIST)

    else:
        break



