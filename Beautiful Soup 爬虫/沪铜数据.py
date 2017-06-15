'''
获取新浪网 沪铜CUO历史交易记录
从1999-01-01 到 2017-06-15
网址：http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=1&breed=CU0&start=1999-01-01&end=2017-06-15&jys=shfe&pz=CU&hy=CU0&type=inner&name=%A1%E4%A8%AE%26%23182%3B11109
'''

import  requests
from bs4 import BeautifulSoup

def get_html_text(url):
    try:
        r = requests.get(url,timeout=3)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'something wrong'



def get_one_data(url):
    data = []
    html = get_html_text(url)
    soup = BeautifulSoup(html,'lxml')
    days = soup.find('div',class_='historyList')
    columns = days.find_all('tr')
    
    '''
    test area:
    info = columns[2].find_all('td')
    date = info[0].text
    close_price = info[1].text
    print(date,close_price)
    '''
    
    for i in range(2,len(columns)):
        try:
            info = columns[i].find_all('td')
            date = info[0].text
            close_price = info[1].text
            data.append(date+' : '+close_price)
        except:
            continue
    
    return data
    
def W2File(data):
    with open('cuo_data.txt','a+') as f:
        for one in data:
            f.write(one+'\n')
    
    print('数据写入完毕！')

#url = 'http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=1&breed=CU0&start=1999-01-01&end=2017-06-15&jys=shfe&pz=CU&hy=CU0&type=inner&name=%A1%E4%A8%AE%26%23182%3B11109'
urls = []

for i in range(1,77):
    urls.append('http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page='+str(i)+'&breed=CU0&start=1999-01-01&end=2017-06-15&jys=shfe&pz=CU&hy=CU0&type=inner&name=%A1%E4%A8%AE%26%23182%3B11109')


for url in urls:
    data = get_one_data(url)
    W2File(data)