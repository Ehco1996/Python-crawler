import shutil

import requests


def get_image(url, path):
    res = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        shutil.copyfileobj(res.raw, f)


def save_html(text, name):
    with open(name, 'w') as f:
        f.write(text)
