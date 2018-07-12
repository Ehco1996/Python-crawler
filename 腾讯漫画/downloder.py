import os
import json

import requests


def download_img(name, url):
    with open(name, 'wb') as f:
        f.write(requests.get(url).content)


def download_comic(comic_name, comic_id):

    # 读取漫画信息
    json_file_name = "{}.json".format(comic_id)
    with open(json_file_name, 'r') as f:
        data = json.load(f)

    # 创建漫画目录
    if not os.path.exists(comic_name):
        os.mkdir(comic_name)

    for k, v in data.items():
        title = k + '-' + v['title']

        # 创建章节目录
        path = os.path.join(comic_name, title)
        if not os.path.exists(path):
            os.mkdir(path)
        for index, v in enumerate(v['pics']):
            name = os.path.join(path, "{}.png".format(index))
            download_img(name, v['url'])
        print(title, '下载完毕')


def main():
    comic_name = "女巫"
    comic_id = 632784
    print('开始下载漫画：', comic_name)
    download_comic(comic_name, comic_id)


if __name__ == '__main__':
    main()
