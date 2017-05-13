# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
import json
import codecs
import pymysql


class WeatherPipeline(object):
    def process_item(self, item, spider):
        '''
        处理每一个从SZtianqi传过来的
        item
        '''
        base_dir = os.getcwd()
        fiename = base_dir + '/data/weather.txt'

        with open(fiename, 'a') as f:
            f.write(item['date'] + '\n')
            f.write(item['week'] + '\n')
            f.write(item['temperature'] + '\n')
            f.write(item['weather'] + '\n')
            f.write(item['wind'] + '\n\n')

        with open(base_dir + '/data/' + item['date'] + '.png', 'wb') as f:
            f.write(requests.get(item['img']).content)

        return item


class W2json(object):
    def process_item(self, item, spider):
        '''
        讲爬取的信息保存到json
        方便其他程序员调用
        '''
        base_dir = os.getcwd()
        filename = base_dir + '/data/weather.json'

        with codecs.open(filename, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(line)

        return item


class W2mysql(object):
    def process_item(self, item, spider):
        '''
        将爬取的信息保存到mysql
        '''

        # 将item里的数据拿出来
        date = item['date']
        week = item['week']
        temperature = item['temperature']
        weather = item['weather']
        wind = item['wind']
        img = item['img']

        # 和本地的scrapyDB数据库建立连接
        connection = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',        # 自己的mysql用户名
            passwd='********',  # 自己的密码
            db='scrapyDB',      # 数据库的名字
            charset='utf8mb4',     # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # 创建更新值的sql语句
                sql = """INSERT INTO WEATHER(date,week,temperature,weather,wind,img)
                        VALUES (%s, %s,%s,%s,%s,%s)"""
                #sql = "INSERT INTO weather (date, week, temperature, weather, wind, img) VALUES (%s, %s,%s,%s,%s,%s)"
                # 执行sql语句
                cursor.execute(
                    sql, (date, week, temperature, weather, wind, img))

            # 提交本次插入的记录
            connection.commit()
        finally:
            # 关闭连接
            connection.close()

        return item
