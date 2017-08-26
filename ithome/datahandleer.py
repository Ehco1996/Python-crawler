'''
热评数据处理

数据： apple.json  苹果分类下的新闻热评 共3672条数据
字段： <id, name, content, phone_com, phone_model, loc, time>
'''

import json

# 读取json数据
with open('apple.json', 'r') as f:
    data = json.load(f)


def city_count(data):
    '''
    统计城市出现次数
    return city
    '''

    city = {}
    for i in data:
        loc = i['loc']
        if loc in city.keys():
            city[loc] += 1
        else:
            city[loc] = 1
    return city


'''
# 获取所有城市出现的次数
city = city_count(data)
#  找到出现最多的前10名
top_city = sorted(city.items(), key=lambda d: d[1], reverse=True)[:10]

# 分离数据，方便生成图片
name = [k for k, v in top_city]
count = [v for k, v in top_city]
print(name)
print(count)
'''


def field_ount(data, field):
    '''
    统计数据中字段名出现的次数
    return dic
    '''

    dic = {}

    for i in data:
        f = i[field]
        if f in dic.keys():
            dic[f] += 1
        else:
            dic[f] = 1
    return dic


def find_top10(dic):
    '''
    找到传进字典的前10名
    并返回对应的 key value list
    '''
    top = sorted(dic.items(), key=lambda d: d[1], reverse=True)[:10]
    name = [k for k, v in top]
    count = [v for k, v in top]
    return name, count


'''
# 获取所有手机厂商
phone_com = field_ount(data,'phone_com')
name,count = find_top10(phone_com)
print(name,count)
'''

'''
# 获取所有手机型号
phone_model = field_ount(data,'phone_model')
name,count = find_top10(phone_model)
print(name,count)
'''


def field_ount_time(data, field):
    '''
    统计数据中字段名出现的次数
    return dic
    对于时间特殊处理
    '''

    dic = {}

    for i in data:
        f = i[field].split(':')[0] + '点'
        if f in dic.keys():
            dic[f] += 1
        else:
            dic[f] = 1
    return dic


'''
# 获取所有发帖时间
time = field_ount_time(data,'time')
name,count = find_top10(time)
print(name,count)
'''

'''
# 获取热评大佬
people = field_ount(data,'name')
name,count = find_top10(people)
print(name,count)
'''

# 检测一下有没重复的段子也能上热评？
p = field_ount(data, 'content')
name, count = find_top10(p)

for duanzi in name:
    print(duanzi)
    print('\n')
