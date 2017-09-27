'''
老司机开车
爬取悦美整形前后对比图


'''
import os
import requests
from bs4 import BeautifulSoup


def get_html_text(url, timeout=5):
    '模拟get请求，获取页面'
    try:
        r = requests.get(url)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def get_html_text_with_post(url, timeout=5):
    '''模拟post请求，获取页面'''
    try:
        r = requests.post(url)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def parse_url_list(url):
    '''
    返回chest页面下
    所有diary的超链接
    rtype： list
    '''
    url_list = []
    html = get_html_text_with_post(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        urls = soup.find_all('a', class_='list-link')
        for url in urls:
            # 针对 //www.yuemei.com/c/1711873.html 格式进行特殊处理
            url_list.append('http:' + url['href'])
    else:
        print('错误发生了！')

    return url_list


def parse_img_package(url):
    '''
    接收dairy的具体url
    解析出该页面的所有高清大图
    和页面用户名
    rtype: dic
    '''
    img_list = []
    html = get_html_text(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # 解析name
        name = soup.find('div', class_='diary-data').span.text
        # 解析图片url
        basediv = soup.find_all('div', class_='list-imgs ')
        for img in basediv:
            urls = img['data-src'].split('//')
            for url in urls:
                if len(url) > 0:
                    img_list.append('http://' + url.replace(',', ''))
        # 将名字和图片链接打包
        print('图包:{} 解析完毕'.format(name))
        return dict(urls=img_list, name=name)
    else:
        print('出错啦！！！')
        return 'error'


def img_downloader(package):
    '''
    下载图片到目录
    接受参数： <dic> package{name,urls}
    当前页面的name，和所有图片的链接
    '''
    dirname = BASE_DIR + 'imgs/' + package['name']

    # 创建对应的文件夹
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        # 开始下载图片
        for url in package['urls']:
            filename = url.split('/')[-1]
            open(dirname + '/' + filename, 'wb').write(requests.get(url).content)
            print('正在下载:{}'.format(filename))
        print('{}图包下载完毕！'.format(package['name']))
    else:
        print('该图包已经下载过了')


# 用列表推导生成我们的入口url  （0 ~ 50页）
base_enter_url = 'http://note.yuemei.com/chest/p{}.html'
enter_url_list = [base_enter_url.format(i) for i in range(1, 51)]
# 获取当前文件运行的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'


if __name__ == '__main__':
        
    # 初始化package列表
    packages = []
    # 获取（5~9）页diary的地址：
    for url in enter_url_list[5:10]:
        diarys = parse_url_list(url)
        for diary_url in diarys:
            # 解析package，并存入列表
            package = parse_img_package(diary_url)
            if package != 'error':
                packages.append(package)

    # 下载图片耗时较长
    # 开启多进程模式
    from multiprocessing import Pool
    # 建立进程池，我cpu是四核的，就是四个进程
    pool = Pool()
    # 进程池，开始批量下载
    pool.map(img_downloader, packages)
    pool.close()
    pool.join()
    
