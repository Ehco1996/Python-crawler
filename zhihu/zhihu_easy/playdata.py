'''
尝试分析用户动态
'''
from datetime import datetime

from lazyspider.lazystore import LazyMysql
from configs import LOCAL_DB

# 建立数据库连接
store = LazyMysql(LOCAL_DB)


def find_most_like(sql):
    '''
    从结果中删选出最受欢迎的内容（前十名）
    基本算法逻辑：
        取出重复出现次数最多的问题
    '''
    res = store.query(sql)
    # 删选重复出现的问题 并取出前10名
    cahe = {}
    for data in res:
        if data['question_id'] not in cahe:
            cahe[data['question_id']] = 0
        else:
            cahe[data['question_id']] += 1
    top10_id = sorted(
        cahe.items(), key=lambda item: item[1], reverse=True)[:10]
    top10_question = []
    for item in top10_id:
        _ = store.find_by_field('zhihu_activities', 'question_id', item[0])[0]
        _.update({'repeat': item[1]})
        top10_question.append(_)
    return top10_question


def find_by_date(start, end):
    '''
    通过时间来筛选数据
    args:
        start/end <datetime>
    '''
    sql = "SELECT * FROM `EhcoTestDb`.`zhihu_activities` WHERE `create_time` BETWEEN '{}' AND '{}'".format(
        start, end)
    res = find_most_like(sql)
    # res = store.query(sql)
    return res


def most_vote_up():
    '''按照回答赞同数量排序 前10名'''
    sql = "SELECT * FROM `EhcoTestDb`.`zhihu_activities` ORDER BY `answer_voteup_count` DESC LIMIT 0, 10"
    res = store.query(sql)
    return res


def most_repeat():
    '''按照相同问题的出现次数排序'''
    sql = "SELECT * FROM `EhcoTestDb`.`zhihu_activities` WHERE `answer_voteup_count` > '100'"
    res = find_most_like(sql)
    return res


def want_to_vote():
    '''轮子哥会给哪些问题点赞'''
    sql = "SELECT * FROM `EhcoTestDb`.`zhihu_activities` WHERE `verb` = 'ANSWER_VOTE_UP' AND `answer_voteup_count` > '100'"
    res = find_most_like(sql)
    return res


def want_to_answer():
    '''轮子哥会回答哪些问题'''
    sql = "SELECT * FROM `EhcoTestDb`.`zhihu_activities` WHERE `verb` = 'ANSWER_CREATE' AND `answer_voteup_count` > '100'"
    res = find_most_like(sql)
    return res


def want_to_follow():
    '''轮子哥会关注哪些问题'''
    sql = "SELECT * FROM `EhcoTestDb`.`zhihu_activities` WHERE `verb` = 'QUESTION_FOLLOW'"
    res = find_most_like(sql)
    return res


def find_girl():
    '''轮子哥喜欢的妹纸'''
    sql = "SELECT * FROM `EhcoTestDb`.`zhihu_activities` WHERE `question_name` LIKE '%妹%' OR `question_name` LIKE '%腿%' OR `question_name` LIKE '%女%' ORDER BY `verb`"
    res = find_most_like(sql)
    return res


res = find_girl()

for item in res:
    url = 'https://www.zhihu.com/question/' + item['question_id']
    print(item['question_name'],url)
