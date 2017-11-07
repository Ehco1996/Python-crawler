'''
对抓取的影评数据
进行基本的分析统计
最后并生成词云
'''

'''
01 最早时间 - - 因为国内外上映时间不一
    统计哪天的评论数量最多
02 推荐程度 - - 前10000 频率统计
03 评论内容 - - 前100 评论内容词频分析，做成词云

'''
# 导入配置文件和数据库支持
import config
from stroe import DbToMysql
from datetime import datetime
import jieba

# 初始化数据库链接
store = DbToMysql(config.EHCO_DB)


def format_to_week(day):
    '''
    将形如这样的日期转换为周x
    '''
    day_map = {
        0: '周一',
        1: '周二',
        2: '周三',
        3: '周四',
        4: '周五',
        5: '周六',
        6: '周日',
    }
    week = datetime.strptime(day, "%Y-%m-%d").weekday()
    return day_map[week]



# 统计评论出现的日期，不同日期下出现的评论数量
date_list = store.find_all('GodOfHammer_1', 19000)

# 建立统计dict
dateSet = {}
for data in date_list:
    week = format_to_week(data['time'])
    if week not in dateSet.keys():
        dateSet[week] = 1
    else:
        dateSet[week] += 1
print(dateSet)
'''
结果：
{'周三': 192, '周四': 234, '周五': 4518, '周二': 109, '周六': 6219, '周日': 5441, '周一': 2287}
'''

'''
# 查询点赞数量排名钱10000的留言的 推荐程度
recommend_level_list = store.find_by_sort('GodOfHammer_1', 'vote', 10000)

# 建立统计dict
recommendSet = {}
# 开始统计不同推荐程度出现的次数
for data in recommend_level_list:
    if data['star'] not in recommendset.keys():
        recommendSet[data['star']] = 1
    else:
        recommendSet[data['star']] += 1
print(recommendSet)
'''

'''

# 截取前100条热门评论并进行分词统计
comment_data = store.find_by_sort('GodOfHammer_1', 'vote', '100')
comment_detail_list = []
for data in comment_data:
    comment_detail_list.append(data['content'])
# 利用结巴分词工具分词
seg_list = jieba.cut(' '.join(comment_detail_list))
for word in seg_list:
    print (word)
'''


