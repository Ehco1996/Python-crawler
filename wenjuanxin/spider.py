import time
from datetime import datetime
from random import randint

from requests_html import HTMLSession

from configs import (QUESTION_ID, QUESTION_URL, POST_URL_MAP,
                     QUESTION_INFO, ANSWER_TIMES)


def parse_post_url(resp):
    '''
    解析出提交问卷的url
    '''
    # 找到rn
    rn = int(resp.html.search('rndnum="{}"')[0].split('.')[0])
    # 提交问卷的时间
    raw_t = round(time.time(), 3)
    t = int(str(raw_t).replace('.', ''))
    # 模拟开始答题时间
    starttime = datetime.fromtimestamp(
        int(raw_t) - randint(1, 60 * 3)).strftime("%Y/%m/%d %H:%M:%S")

    url = POST_URL_MAP.format(QUESTION_ID, t, starttime, rn)
    return url


def parse_post_data(resp):
    '''
    解析出问题和选项
    返回post_data
    '''
    post_data = {'submitdata': ""}
    questions = resp.html.find('fieldset', first=True).find('.div_question')

    for i, q in enumerate(questions):
        title = q.find('.div_title_question_all', first=True).text
        choices = [t.text for t in q.find('label')]
        random_index = randint(0, len(choices) - 1)
        choice = choices[random_index]
        post_data['submitdata'] += '{}${}}}'.format(i+1, random_index+1)
        print(QUESTION_INFO.format(title, choices, choice))
        time.sleep(0.5)
    # 去除最后一个不合法的`}`
    post_data['submitdata'] = post_data['submitdata'][:-1]
    return post_data


def post_answer(session, url, data):
    '''
    提交答案
    '''
    r = session.post(url, data)
    print('提交状态：{}'.format(r.status_code))


def simulate_survey():
    '''
    模拟回答问卷
    '''
    session = HTMLSession()
    resp = session.get(QUESTION_URL)
    url = parse_post_url(resp)
    data = parse_post_data(resp)
    post_answer(session, url, data)


def main():
    print('开始模拟填写问卷,共模拟{}次'.format(ANSWER_TIMES))
    for i in range(ANSWER_TIMES):
        simulate_survey()
        sleep_time = randint(1, 60)
        print('第{}次问卷填写完毕，即将沉睡{}s'.format(i+1, sleep_time))
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
