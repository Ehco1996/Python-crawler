'''
处理数据
保存到mogodb
'''

from pymongo import MongoClient
from config import *

client = MongoClient(MONGO_URL, connect=True)
db = client[MONGO_DB]

# 将记录写入数据库
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储成功', result)
        return True
    return False


