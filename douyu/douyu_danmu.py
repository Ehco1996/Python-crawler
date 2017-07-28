'''
利用斗鱼弹幕 api
尝试抓取斗鱼tv指定房间的弹幕
'''

import multiprocessing
import socket
import time
import re
import signal

# 构造socket连接，和斗鱼api服务器相连接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))

# 弹幕查询正则表达式
danmu_re = re.compile(b'txt@=(.+?)/cid@')
username_re = re.compile(b'nn@=(.+?)/txt@')


def send_req_msg(msgstr):
    '''构造并发送符合斗鱼api的请求'''

    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    # 构造协议头
    msgHead = int.to_bytes(data_length, 4, 'little') \
        + int.to_bytes(data_length, 4, 'little') + \
        int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


def DM_start(roomid):
    # 构造登录授权请求
    msg = 'type@=loginreq/roomid@={}/\0'.format(roomid)
    send_req_msg(msg)
    # 构造获取弹幕消息请求
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    send_req_msg(msg_more)

    while True:
        # 服务端返回的数据
        data = client.recv(1024)
        # 通过re模块找发送弹幕的用户名和内容
        danmu_username = username_re.findall(data)
        danmu_content = danmu_re.findall(data)
        if not data:
            break
        else:
            for i in range(0, len(danmu_content)):
                try:
                    # 输出信息
                    print('[{}]:{}'.format(danmu_username[0].decode(
                        'utf8'), danmu_content[0].decode(encoding='utf8')))
                except:
                    continue


def keeplive():
    '''
    保持心跳，15秒心跳请求一次
     '''
    while True:
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        send_req_msg(msg)
        print('发送心跳包')
        time.sleep(15)


def logout():
    '''
    与斗鱼服务器断开连接
    关闭线程
    '''
    msg = 'type@=logout/'
    send_req_msg(msg)
    print('已经退出服务器')


def signal_handler(signal, frame):
    '''
    捕捉 ctrl+c的信号 即 signal.SIGINT
    触发hander：
    登出斗鱼服务器
    关闭进程
    '''
    p1.terminate()
    p2.terminate()
    logout()
    print('Bye')


if __name__ == '__main__':
    #room_id = input('请输入房间ID： ')

    # 狗贼的房间号
    room_id = 208114
    # 开启signal捕捉
    signal.signal(signal.SIGINT, signal_handler)

    # 开启弹幕和心跳进程
    p1 = multiprocessing.Process(target=DM_start, args=(room_id,))
    p2 = multiprocessing.Process(target=keeplive)
    p1.start()
    p2.start()
