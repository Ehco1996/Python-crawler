# -*- coding: utf-8 -*-
import struct
import os
import time
import sys

from queue import Queue
from threading import Thread
from pypinyin import lazy_pinyin

PROJECT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'sougou'))

import configs
from store_new.stroe import DbToMysql


# 建立一个线程池 用于存入解析完毕的数据
res_queue = Queue()


class ExtSougouScel():
    '''
    解析搜狗词库文件
    '''

    def __init__(self):
        # 拼音表偏移，
        self.startPy = 0x1540
        # 汉语词组表偏移
        self.startChinese = 0x2628
        # 全局拼音表
        self.GPy_Table = {}
        # 解析结果
        # 元组(词频,拼音,中文词组)的列表
        self.GTable = []

    def byte2str(self, data):
        '''将原始字节码转为字符串'''
        i = 0
        length = len(data)
        ret = ''
        while i < length:
            x = data[i:i + 2]
            t = chr(struct.unpack('H', x)[0])
            if t == '\r':
                ret += '\n'
            elif t != ' ':
                ret += t
            i += 2
        return ret

    def getPyTable(self, data):
        '''获取拼音表'''

        # if data[0:4] != "\x9D\x01\x00\x00":
        #     return None
        data = data[4:]
        pos = 0
        length = len(data)
        while pos < length:
            index = struct.unpack('H', data[pos:pos + 2])[0]
            # print index,
            pos += 2
            l = struct.unpack('H', data[pos:pos + 2])[0]
            # print l,
            pos += 2
            py = self.byte2str(data[pos:pos + l])
            # print py
            self.GPy_Table[index] = py
            pos += l

    def getWordPy(self, data):
        '''获取一个词组的拼音'''
        pos = 0
        length = len(data)
        ret = u''
        while pos < length:
            index = struct.unpack('H', data[pos] + data[pos + 1])[0]
            ret += self.GPy_Table[index]
            pos += 2
        return ret

    def getWord(self, data):
        '''获取一个词组'''
        pos = 0
        length = len(data)
        ret = u''
        while pos < length:

            index = struct.unpack('H', data[pos] + data[pos + 1])[0]
            ret += self.GPy_Table[index]
            pos += 2
        return ret

    def getChinese(self, data):
        '''读取中文表'''
        pos = 0
        length = len(data)
        while pos < length:
            # 同音词数量
            # same = struct.unpack('H', data[pos] + data[pos + 1])[0]
            same = struct.unpack('H', data[pos:pos + 2])[0]
            # 拼音索引表长度
            pos += 2
            # py_table_len = struct.unpack('H', data[pos] + data[pos + 1])[0]
            py_table_len = struct.unpack('H', data[pos:pos + 2])[0]
            # 拼音索引表
            pos += 2
            # py = getWordPy(data[pos: pos+py_table_len])
            # 中文词组
            pos += py_table_len
            for i in range(same):
                # 中文词组长度
                # c_len = struct.unpack('H', data[pos] + data[pos + 1])[0]
                c_len = struct.unpack('H', data[pos:pos + 2])[0]
                # 中文词组
                pos += 2
                word = self.byte2str(data[pos: pos + c_len])
                # 扩展数据长度
                pos += c_len
                # ext_len = struct.unpack('H', data[pos] + data[pos + 1])[0]
                ext_len = struct.unpack('H', data[pos:pos + 2])[0]
                # 词频
                pos += 2
                # count = struct.unpack('H', data[pos] + data[pos + 1])[0]
                count = struct.unpack('H', data[pos:pos + 2])[0]
                # 保存
                # GTable.append((count,py,word))
                self.GTable.append(word)
                # 到下个词的偏移位置
                pos += ext_len

    def deal(self, file_name):
        '''处理文件'''
        print('-' * 60)
        f = open(file_name, 'rb')
        data = f.read()
        f.close()
        if data[0:12] != b'@\x15\x00\x00DCS\x01\x01\x00\x00\x00':
            print("确认你选择的是搜狗(.scel)词库?")
            sys.exit(0)
        print("词库名：", self.byte2str(data[0x130:0x338]))
        # print("词库类型：", self.byte2str(data[0x338:0x540]))
        # print("描述信息：", self.byte2str(data[0x540:0xd40]))
        # print("词库示例：", self.byte2str(data[0xd40:self.startPy]))
        # self.getPyTable(data[self.startPy:self.startChinese])
        self.getChinese(data[self.startChinese:])
        # 返回解析完毕的所有中文词组
        return list(sorted(set(self.GTable), key=self.GTable.index))


def ext_to_queue():
    '''
    遍历目录下的所有词库文件
    解析文件存入Queue
    '''
    # 词库文件目录
    path1 = '/Users/ehco/Desktop/input/'
    for filename in os.listdir(path1):
        # 解析一级二级目录
        type1 = filename.split('_')[0]
        type2 = filename.split('_')[1]
        type3 = filename.split('_')[2].split('.')[0]
        # 将关键字解析 拼成字典存入queue
        words_data = ExtSougouScel().deal(path1 + filename)
        # 判断队列大小，若太大就停止从目录读文件
        s = res_queue.qsize()
        print("size", s)
        while s > 40000:
            print("sleep for a while ")
            time.sleep(20)
            s = res_queue.qsize()
            print('new size is {}'.format(s))
        for word in words_data:
            '''
            解析每一条数据，并存入队列
            '''
            keyword = word
            pinyin = " ".join(lazy_pinyin(word))
            data = {
                'keyword': keyword,
                'pinyin': pinyin,
                'type1': type1,
                'type2': type2,
                'type3': type3,
            }
            res_queue.put_nowait(data)
    print('all file finshed')


def save_data(data, store):
    '''
    存入一条记录进数据库
    '''
    store.save_one_data('keyword_sogou', data)


def save_to_db():
    '''
    从数据队列里拿一条数据
    并存入数据库
    '''
    store = DbToMysql(configs.TEST_DB)
    while True:
        try:
            st = time.time()
            data = res_queue.get_nowait()
            t = int(time.time() - st)
            if t > 5:
                print("res_queue", t)
            save_data(data, store)
        except:
            print("queue is empty wait for a while")
            time.sleep(2)


def start():
    # 使用多线程解析
    threads = list()
    # 读文件存入queue的线程
    threads.append(
        Thread(target=ext_to_queue))

    # 存数据库的线程
    for i in range(10):
        threads.append(
            Thread(target=save_to_db))
    for thread in threads:
        thread.start()


if __name__ == '__main__':
    start()
