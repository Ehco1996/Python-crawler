'''
爬取悦音台mv排行榜，以及一点点反爬虫技术。
使用 requests --- bs4 线路
Python版本： 3.6
OS： mac os 12.12.4
'''
import requests
import bs4
import random


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Someting Wrong！"


def get_agent():
    '''
    模拟header的user-agent字段，
    返回一个随机的user-agent字典类型的键值对
    '''
    agents = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
    fakeheader = {}
    fakeheader['User-agent'] = agents[random.randint(0, len(agents))]
    return fakeheader


def get_proxy():
    '''
    简答模拟代理池
    返回一个字典类型的键值对，
    '''
    proxy = ["http://116.211.143.11:80",
             "http://183.1.86.235:8118",
             "http://183.32.88.244:808",
             "http://121.40.42.35:9999",
             "http://222.94.148.210:808"]
    fakepxs = {}
    fakepxs['http'] = proxy[random.randint(0, len(proxy))]
    return fakepxs


def get_content(url):
    #我们来打印一下表头
    if url[-2:]=="ML":
        print("内地排行榜")
    elif url[-2:]=="HT":
        print("香港排行榜")
    elif url[-2:]=="US":
        print("欧美排行榜")
    elif url[-2:]=="KR":
        print("韩国排行榜")
    else:
        print("日本排行榜")

    # 找到我们需要的每个li标签
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    li_list = soup.find_all('li', attrs={'name': 'dmvLi'})
     
    for li in li_list:
        match = {}
        try:
            #判断分数的升降！
            if li.find('h3', class_='desc_score'):
                match['分数'] = li.find('h3', class_='desc_score').text
            else:
                match['分数'] = li.find('h3', class_='asc_score').text
            
            match['排名'] = li.find('div', class_='top_num').text
            match['名字'] = li.find('a', class_='mvname').text
            match['发布时间'] = li.find('p', class_='c9').text
            match['歌手'] = li.find('a', class_='special').text
        except:
            return ""
        print(match)






def main():
    base_url = "http://vchart.yinyuetai.com/vchart/trends?area="
    suffix = ['ML','HT','US','JP','KR']
    for suff in suffix:
        url = base_url+suff
        print()
        get_content(url)


if __name__ == '__main__':
    main()
