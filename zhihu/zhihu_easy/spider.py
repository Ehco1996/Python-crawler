import json
import time
import os

from client import ZhihuClient
from configs import USERNAME, PASSWD, AUTH, START_URL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def download_activs_json(s, url, count=1):
    '''
    获取用户信息的json信息
    '''
    res = s.get(url).json()
    with open(BASE_DIR+'/data/{}.json'.format(count), 'w') as f:
        f.write(json.dumps(res, ensure_ascii=False))
    print('正在下载第{}份动态'.format(count))
    count += 1
    time.sleep(1)
    # 递归下载 直到动态下载完毕
    if res['paging']['is_end'] == False:
        next_url = res['paging']['next']
        download_activs_json(s, next_url, count)
    else:
        print('所有动态下载完毕')


def download_activs():
    # 登录知乎
    s = ZhihuClient(USERNAME, PASSWD).get_session()
    # 增加权限认证
    s.headers.update({'authorization': AUTH})
    download_activs_json(s, START_URL)


if __name__ == "__main__":
    download_activs()
