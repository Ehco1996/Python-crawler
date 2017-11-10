'''
Author Ehco1996
Time 2017-11-10

如何暗示男朋友给自己买火红
'''

from bs4 import BeautifulSoup
import requests
import os


def get_html_text(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status
        return r.text
    except:
        return -1


def parse_img(html):
    data = []
    soup = BeautifulSoup(html, 'lxml')
    img_list = soup.find_all('img')
    for img in img_list:
        data.append({
            'src': img['src'],
            'name': img['alt'].replace(' ', '').replace('/', '')
        })
    return data


def get_img_response(url):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status
        return r.content
    except:
        return -1


def download_img(data):
    curr_dir = os.path.dirname(os.path.realpath(__file__)) + '/img/'
    if not os.path.exists('img'):
        os.mkdir('img')
    for img in data:
        path = os.path.join(curr_dir, img['name'] + '.jpg')
        with open(path, 'wb') as f:
            f.write(get_img_response(img['src']))


def main():
    html = get_html_text(
        'https://www.1688.com/pic/-.html?spm=a261b.8768355.searchbar.5.oUjRZK&keywords=%BF%DA%BA%EC')
    if html != -1:
        img_data = parse_img(html)
        download_img(img_data)


if __name__ == '__main__':
    main()
