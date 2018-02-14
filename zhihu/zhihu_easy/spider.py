import json
import time
import os

from client import ZhihuClient

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
    time.sleep(3)
    # 递归下载 知道动态下载完毕
    if res['paging']['is_end'] == False:
        next_url = res['paging']['next']
        download_activs_json(s, next_url, count)
    else:
        print('所有动态下载完毕')


# 登录知乎
s = ZhihuClient('', '').get_session()
# 增加权限认证
s.headers.update({'authorization': ''})
# 起始动态url
start_url = 'https://www.zhihu.com/api/v4/members/Ehcostuff/activities?limit=8&after_id=1518305424&desktop=True'
download_activs_json(s, start_url)
