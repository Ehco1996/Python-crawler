'''
将数据存入数据库模块
'''

import pymysql.cursors

import config


class DbToMysql():
    '''封装对数据库的操作'''

    def __init__(self, configs):
        self.con = pymysql.connect(
            host=configs['host'],
            user=configs['user'],
            password=configs['password'],
            db=configs['db'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        '''关闭数据库链接'''
        self.con.close()

    def save_one_data(self, table, data,):
        '''
        将一条记录保存到数据库
        Args: 
            table: 表名字 str
            data:  记录 dict
        每条记录都以一个字典的形式传进来
        '''
        key_map = {}

        if len(data) == 0:
            return -1

        fields = ''
        values = ''
        datas = {}
        for k, v in data.items():
            # 防止sql注入
            datas.update({k: pymysql.escape_string(v)})
        
        for d in datas:
            fields += "`{}`,".format(str(d))
            values += "'%s'," % (str(data[d]))
        if len(fields) <= 0 or len(values) <= 0:
            return -1
        # 生成sql语句
        sql = "insert ignore into {}({}) values({})".format(
            table, fields[:-1], values[:-1])

        try:
            with self.con.cursor() as cursor:
                # 执行语句
                cursor.execute(sql)
                self.con.commit()
                res = cursor.fetchone()
                return res
        except:
            print('数据库保存错误')
