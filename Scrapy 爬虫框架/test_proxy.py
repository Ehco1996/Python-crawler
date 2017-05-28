'''
我们通过这个小脚本来判断
抓取到的ip代理是否可以用！

还是通过我最熟悉的request库来实现
不过这里稍微加一下我也不太熟悉的多线程
'''

import requests

# 引入这个库来获得map函数的并发版本
from multiprocessing.dummy import Pool as ThreadPool

# 定义全局变量
dir_path = '/Users/ehco/Desktop/result/'
alive_ip = []

# 使得map并发！实例化pool对象
pool = ThreadPool()
# 设置并发数量！
pool = ThreadPool(20)


def test_alive(proxy):
    '''
    一个简单的函数，
    来判断通过代理访问百度
    筛选通过的代理保存到alive_ip中
    '''
    global alive_ip
    proxies = {'http': proxy}
    print('正在测试：{}'.format(proxies))
    try:
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=3)
        if r.status_code == 200:
            print('该代理：{}成功存活'.format(proxy))
            alive_ip.append(proxy)
    except:
        print('该代理{}失效！'.format(proxies))


def Out_file(alive_ip=[]):
    global dir_path
    with open(dir_path + 'alive_ip.txt', 'a+') as f:
        for ip in alive_ip:
            f.write(ip + '\n')
        print('所有存活ip都已经写入文件！')


def test(filename='blank.txt'):
    # 循环处理每行文件
    with open(dir_path + filename, 'r') as f:
        lines = f.readlines()
        # 我们去掉lines每一项后面的\n\r之类的空格
        # 生成一个新的列表！
        proxys = list(map(lambda x: x.strip(), [y for y in lines]))

        #一行代码解决多线程！
        pool.map(test_alive,proxys)
        pool.close()
        pool.join()
       
    # 将存活的ip写入文件
    Out_file(alive_ip)


#调用函数！
test('kdl_proxy.txt')
