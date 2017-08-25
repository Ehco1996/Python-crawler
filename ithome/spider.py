'''
it 之家热评抓取
'''


import requests
from bs4 import BeautifulSoup
# 导入数据库存储方法
from pipeline import save_to_mongo


def parse_hot_comment(newsid):
    '''
    找到it之家新闻的热评

    return :info_list <list>
    '''
    info_list = []
    data = {
        'newsID': newsid,
        'type': 'hotcomment'
    }
    try:
        r = requests.post(
            'https://dyn.ithome.com/ithome/getajaxdata.aspx', data=data)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        comment_list = soup.find_all('li', class_='entry')
        for comment in comment_list:
            # 评论内容
            content = comment.find('p').text
            # 用户名
            name = comment.find('strong', class_='nick').get_text()
            # 其他信息
            info = comment.find('div', class_='info rmp').find_all('span')
            # 判断用户是否填写了手机尾巴
            # 对信息做出咸蛋的处理
            # 抓取到 手机厂商、型号、位置、时间
            # 方便最后做数据分析
            if len(info) > 1:
                phone_com = info[0].text.split(' ')[0]
                phone_model = info[0].text.split(' ')[1]
                loc = info[1].text.replace('IT之家', '').replace(
                    '网友', ' ').replace('\xa0', '').split(' ')[0]
                time = info[1].text.replace('IT之家', '').replace(
                    '网友', ' ').replace('\xa0', '').split(' ')[2]
            else:
                phone_com = '暂无'
                phone_model = '暂无'
                loc = info[0].text.replace('IT之家', '').replace(
                    '网友', ' ').replace('\xa0', '').split(' ')[0]
                time = info[0].text.replace('IT之家', '').replace(
                    '网友', ' ').replace('\xa0', '').split(' ')[2]

            info_list.append(
                {'name': name, 'content': content, 'phone_com': phone_com, 'phone_model': phone_model, 'loc': loc, 'time': time, })

        return info_list
    except:
        return None


def parse_news_id(categoryid, page_start):
    '''
    找到当前分类下首页的文章的id

    retrun newsid <str>
    '''
    data = {
        'categoryid': categoryid,
        'type': 'pccategorypage',
        'page': '1',
    }

    # 循环获取newsid 最早可到2014年12月
    # 默认每次取10页
    for page in range(page_start, page_start + 11):
        data['page'] = str(page)
        try:
            r = requests.post(
                'http://it.ithome.com/ithome/getajaxdata.aspx', data=data)
            soup = BeautifulSoup(r.text, 'lxml')
            news_list = soup.find_all('a', class_='list_thumbnail')
            # 找到当前页的所有新闻链接之后，用生成器返回newsid
            for news in news_list:
                yield news['href'].split('/')[-1].replace('.htm', '')

        except:
            return None


import time

# 写了一个检测函数运行时间的装饰器
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)  # 装饰被装饰的函数

        timepassed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)

        print('[{:.8f}s]   {}({})  -> {}'.format(timepassed, name, arg_str, result))
    return clocked


#@clock
def main(page_start):
    # 新闻分类的id
    ID = '31'
    # 建立苹果新闻分类对象
    apple = parse_news_id(ID, page_start)

    # 利用迭代器抓取热评
    for newsid in apple:
        hot_comment_dic = parse_hot_comment(newsid)
        if hot_comment_dic:
            for comment in hot_comment_dic:
                save_to_mongo(comment)
        else:
            print('没有抓取到热评，一般是文章太过久远')


if __name__ == '__main__':

    # 单进程模式
    # main(1)
    
    # 开启多进程模式
    from multiprocessing import Pool
    pool = Pool()  
    # 进程池，每个进程抓取10页新闻的热评
    groups = ([x for x in range(111, 191,10)])
    pool.map(main, groups)
    pool.close()
    pool.join()



'''
开启多进程之前 ，抓取一页新闻的所有热评所话费的时间
[8.45930967s]   main()  -> None

抓取10页：
[112.86940903s]   main(61)  -> None

开启后：
不能使用装饰器测时间了
AttributeError: Can't pickle local object 'clock.<locals>.clocked'
改为第三方秒表计时：
1~40:

1:56.54
可以看到 速度快了三倍！
'''
