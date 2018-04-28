QUESTION_ID = 11231

QUESTION_URL = "https://www.wjx.cn/jq/{}.aspx".format(QUESTION_ID)

# 提交问卷选项的url
POST_URL_MAP = "https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&curID={}&t={}&starttime={}&rn={}"

QUESTION_INFO = '''
题目：{}
选项：{}

随机选择结果：{}

~~~~~~~~~~~~~~~~~~~~~~
'''

# 回答次数
ANSWER_TIMES = 3
