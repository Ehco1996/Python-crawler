'''
尝试登录支付宝
并获账单记录
'''

import requests
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup


# 自定义headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Referer': 'https://consumeprod.alipay.com/record/advanced.htm',
    'Host': 'consumeprod.alipay.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive'
}


# 将复制到cookies 转换为字典，方便调用
raw_cookies = 'JSESSIONID=RZ13thOM1dM5K05460101";     中间省略了     one=RZ250AATO/mr4CZ1cRnxgFmVR'
cookie = SimpleCookie(raw_cookies)
cookies = {i.key: i.value for i in cookie.values()}


# 尝试使用面向对象的方式来造爬虫
class Alipay_Bill_Info(object):
    '''支付宝账单信息'''

    def __init__(self, headers, cookies):
        '''
        类的初始化

        headers：请求头
        cookies: 持久化访问
        info_list: 存储账单信息的列表
        '''
        self.headers = headers
        self.cookies = cookies
        # 利用requests库构造持久化请求
        self.session = requests.Session()
        # 将请求头和cookies添加到缓存之中
        self.session.headers = self.headers
        self.session.cookies.update(self.cookies)
        self.info_list = []

    def login_status(self):
        '''判断登录状态'''
        status = self.session.get(
            'https://consumeprod.alipay.com/record/standard.htm', timeout=5, allow_redirects=False).status_code
        print(status)
        if status == 200:
            return True
        else:
            return False

    def get_data(self):
        '''
        利用bs4库解析html
        并抓取数据，
        数据以字典格式保存在列表里
        '''
        status = self.login_status()
        url = 'https://consumeprod.alipay.com/record/standard.htm'
        if status:
            html = self.session.get(url).text
            soup = BeautifulSoup(html, 'lxml')
            # 抓取前五个交易记录
            trades = soup.find_all('tr', class_='J-item ')[:5]

            for trade in trades:
                # 做一个try except 避免异常中断
                try:
                    # 分别找到账单的 时间 金额 以及流水号
                    time = trade.find('p', class_='text-muted').text.strip()
                    amount = trade.find(
                        'span', class_='amount-pay').text.strip()
                    code = trade.find(
                        'a', class_='J-tradeNo-copy J-tradeNo')['title']
                    self.info_list.append(
                        dict(time=time, amount=amount, code=code))
                except:
                    self.info_list.append({'error': '出现错误,请加站长支付宝好友获取充值码'})

        else:
            self.info_list.append({'error': '出现错误,请加站长支付宝好友获取充值码'})



# 测试一下：
test = Alipay_Bill_Info(HEADERS, cookies)
test.get_data()

print(test.info_list)

'''
OUT:

200
[{'time': '07:34', 'amount': '- 3.00', 'code': '2017081521001004100329637047'},
    {'time': '07:08', 'amount': '- 100.00', 'code': '2017081521001004100329622812'},
    {'time': '05:37', 'amount': '+ 0.14', 'code': '20170815344111650101'},
    {'time': '01:08', 'amount': '+ 10.00','code': '20170815200040011100040078948930'},
    {'time': '22:23', 'amount': '+ 10.00', 'code': '20170814200040011100060079678223'}]
'''
