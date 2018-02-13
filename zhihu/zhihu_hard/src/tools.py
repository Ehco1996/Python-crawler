import shutil

import requests
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from configs import COOKIES, HEDADERS


def my_session():
    session = requests.Session()
    session.get('https://www.zhihu.com',
                cookies=COOKIES, headers=HEDADERS)
    return session


def get_image(url, path):
    res = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        shutil.copyfileobj(res.raw, f)


def save_html(text, name):
    with open(name, 'w') as f:
        f.write(text)


def get_driver():
    # 设置请求头
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (HEDADERS.get("User-Agent"))
    # 初始化driver
    driver = PhantomJS(desired_capabilities=dcap)
    # 加入cookies
    for c in my_session().cookies:
        driver.add_cookie({'name': c.name, 'value': c.value,
                           'path': c.path, 'expiry': c.expires, 'domain': c.domain})
    # 设置窗口大小
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)
    return driver
