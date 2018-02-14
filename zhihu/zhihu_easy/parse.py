import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_activites(file_path):
    '''
    解析用户动态数据
    rtype:
        list
    '''
    with open(file_path) as f:
        data = json.load(f).get('data')
        res = []
        for action in data:
            verb = action['verb']
            if verb == 'ANSWER_VOTE_UP' or verb == 'ANSWER_CREATE':  # 赞同/回答的行为
                question_id = action['target']['question']['id']
                question_api_url = action['target']['question']['url']
                question_name = action['target']['question']['title']

                answer_id = action['target']['id']
                answer_api_url = action['target']['url']
                answer_content = action['target']['excerpt']
            elif verb == 'QUESTION_FOLLOW':  # 关注问题的行为
                question_id = action['target']['id']
                question_api_url = action['target']['url']
                question_name = action['target']['title']

                answer_id = ''
                answer_api_url = ''
                answer_content = ''
            else:
                continue

            res.append({
                'question_id': question_id,
                'question_name': question_name,
                'question_api_url': question_api_url,
                'answer_id': answer_id,
                'answer_api_url': answer_api_url,
                'answer_content': answer_content, })
        return res


for file in os.listdir(BASE_DIR+'/data/'):
    file_abs_path = BASE_DIR+'/data/'+file
    res = parse_activites(file_abs_path)
    for data in res:
        for k, v in data.items():
            print(k, v)
