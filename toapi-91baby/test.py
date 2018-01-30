'''测试api的使用'''

import sys
import requests
from prettytable import PrettyTable

list_url = 'http://127.0.0.1:5000/hotbook?page={}'
book_url = 'http://127.0.0.1:5000/book_id={}?page={}'


def get_json_response(url):
    r = requests.get(url)
    return r.json()


def print_table(header, rows):
    x = PrettyTable(header)
    for row in rows:
        x.add_row(row)
    print(x)


def get_book_list(page):
    '''获取指定页码的书籍列表'''
    # 获取第一页的所有书籍信息
    page_json = get_json_response(list_url.format(page))
    header = ['书号', '书名', '链接']
    rows = []
    for book in page_json['HotBook']:
        rows.append([book['book_id'], book['title'], book['url']])
    # 打印第一页的信息
    print_table(header, rows)


def get_book_content(book_id, page):
    # 获取书籍信息
    book_json = get_json_response(book_url.format(book_id, page))
    book = book_json['Book']
    # 打印书籍头
    header = ['书名', '作者', '总页数', '当前页']
    rows = [[book['title'], book['author'], book['total_page'], page]]
    print_table(header, rows)
    # 打印书籍内容
    contents = book['contents']
    key = input('要开始看小说么？y键开始\n\n')
    if key == 'y':
        for i in range(len(contents)):
            print(book['title'] + '第{}章节 \n\n'.format(i))
            print(contents[i] + '\n\n')
            input('本章已经阅读完，任意键阅读下一章节！\n\n')
            
        key = input('本页小说已经全部阅读完毕，要看下一页么？y键确定\n\n')
        if key == 'y':
            page += 1
            get_book_content(book_id, page)
    else:
        sys.exit('退出程序...')


def main():
    while True:
        page = input(
            '想看第几页书的书？ 请在下方输入页码 按回车键确定！q键退出 \n\n')
        if page == 'q':
            sys.exit()
        if page == 'y':
            book_id = input('请输入书号阅读书籍: \n')
            page = 1
            get_book_content(book_id, page)
        get_book_list(page)
        print('找到想看的书了？想进去瞧一眼么？输入 y 进入书号输入界面！\n\n')


if __name__ == '__main__':
    main()
