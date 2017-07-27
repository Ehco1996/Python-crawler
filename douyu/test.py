'''
利用斗鱼弹幕 api
尝试抓取斗鱼tv指定房间的弹幕
'''

import multiprocessing
import socket
import time
import re
import requests
from bs4 import BeautifulSoup


# 构造socket连接，和斗鱼api服务器相连接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))

# 弹幕查询正则表达式
danmu_re = re.compile(b'txt@=(.+?)/cid@')


def send_req_msg(msgstr):
    '''构造并发送符合斗鱼api的请求'''
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
        + int.to_bytes(data_length, 4, 'little') + \
        int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


def DM_start(roomid):
    # 构造登录请求
    msg = 'type@=loginreq/roomid@={}/\0'.format(roomid)
    print(msg)
    send_req_msg(msg)
    # 构造获取弹幕消息请求
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    print(msg_more)
    send_req_msg(msg_more)

    while True:
        data = client.recv(1024)
        danmu_more = danmu_re.findall(data)
        print(data)
        if not data:
            break
        else:
            for i in range(0, len(danmu_more)):
                try:
                    print(danmu_more[0].decode(encoding='utf-8'))
                except:
                    continue


def keeplive():
    '''
    保持心跳，30秒心跳请求一次
     '''
    while True:
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        send_req_msg(msg)
        time.sleep(30)


if __name__ == '__main__':
    #room_id = input('请输入房间ID： ')
    room_id = 50552
    p1 = multiprocessing.Process(target=DM_start, args=(room_id,))
    p2 = multiprocessing.Process(target=keeplive)
    p1.start()
    p2.start()
