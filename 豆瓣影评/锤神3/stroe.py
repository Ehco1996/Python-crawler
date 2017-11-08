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
        return:
            成功： dict 保存的记录
            失败： -1
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
            values += "'{}',".format(str(data[d]))
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
            return -1
        finally:
            self.close()

    def find_all(self, table, limit):
        '''
        从数据库里查询所有记录
        Args:
            table: 表名字 str
            limit: 限制数量
        return:
            成功： [dict] 保存的记录
            失败： -1
        '''
        try:
            with self.con.cursor() as cursor:
                sql = "select * from {} limit 0,{}".format(table, limit)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except:
            print('数据查询存错误')
            return -1
        finally:
            self.close()

    def find_by_field(self, table, field, field_value):
        '''
        从数据库里查询指定条件的记录
        Args:
            table: 表名字 str
            field: 字段名
            field_value: 字段值
        return:
            成功： [dict] 保存的记录
            失败： -1
        '''
        try:
            with self.con.cursor() as cursor:
                sql = "select * from {} where {} = '{}'".format(
                    table, field, field_value)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except:
            print('数据查询存错误')
            return -1
        finally:
            self.close()

    def find_by_fields(self, table, queryset={}):
        '''
        从数据库里查询 符合多个条件的记录 
        Args:
            table: 表名字 str
            queryset : key 字段 value 值 dict
        return:
            成功： [dict] 保存的记录
            失败： -1
        '''

        try:
            with self.con.cursor() as cursor:
                querrys = ""
                for k, v in queryset.items():
                    querrys += "{} = '{}' and ".format(k, v)
                sql = "select * from {} where {} ".format(
                    table, querrys[:-4])
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except:
            print('数据查询存错误')
            return -1
        finally:
            self.close()
            

    def find_by_sort(self, table, field, limit=1000, order='DESC'):
        '''
        从数据库里查询排序过的数据
        Args:
            table: 表名字 str
            field: 字段名
            limit: 限制数量
            order: 降序DESC/升序ASC 默认为降序
        return:
            成功： [dict] 保存的记录
            失败： -1
        '''
        try:
            with self.con.cursor() as cursor:
                sql = "select * from {} order by {} {} limit 0,{}".format(
                    table, field, order, limit)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except:
            print('数据查询存错误')
            return -1
        finally:
            self.close()
