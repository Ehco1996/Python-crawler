import json
from datetime import datetime


def parse_activities(file_path):
    '''
    解析用户动态数据
    rtype:
        list
    '''
    with open(file_path) as f:
        try:
            data = json.load(f).get('data')
        except:
            print('{}文件载入失败'.format(file_path))
            return []
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
                answer_voteup_count = action['target']['voteup_count']
                create_time = datetime.fromtimestamp(
                    action['target']['created_time'])

            elif verb == 'QUESTION_FOLLOW':  # 关注问题的行为
                question_id = action['target']['id']
                question_api_url = action['target']['url']
                question_name = action['target']['title']

                answer_id = ''
                answer_api_url = ''
                answer_content = ''
                answer_voteup_count = 0
                create_time = datetime.fromtimestamp(
                    action['target']['created'])

            else:
                continue

            res.append({
                'question_id': question_id,
                'question_name': question_name,
                'question_api_url': question_api_url,
                'answer_id': answer_id,
                'answer_api_url': answer_api_url,
                'answer_content': answer_content,
                'verb': verb,
                'answer_voteup_count': answer_voteup_count,
                'create_time': create_time, })
        return res
