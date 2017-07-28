'''
利用第三方模块：danmu
抓取斗鱼弹幕
'''
import time, sys

from danmu import DanMuClient

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').
        decode(sys.stdin.encoding))

dmc = DanMuClient('https://www.douyu.com/208114')
if not dmc.isValid(): print('Url not valid')

@dmc.danmu
def danmu_fn(msg):
    pp('[%s] %s' % (msg['NickName'], msg['Content']))
'''
@dmc.gift
def gift_fn(msg):
    pp('[%s] sent a gift!' % msg['NickName'])

@dmc.other
def other_fn(msg):
    pp('Other message received')
'''
dmc.start(blockThread = True)