import requests


data = {
    'searchsel': 'forum',
    'mod': 'forum',
    # 'formhash': '88019570',
    'srchtype': 'title',
    'srchtxt': '古代',
    # 'x': '0',
    # 'y': '0',
}


r = requests.post(
    'https://91baby.mama.cn/search.php?searchsubmit=yes', data=data)

print(r.status_code)

print(r.text)
