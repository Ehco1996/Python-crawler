

from configs import COOKIES, HEDADERS
from tools import get_driver
from parse import to_soup


class UserActivities():
    '''
    用户的动态信息
    '''

    def __init__(self, url):
        self.driver = get_driver()
        self.peopple_url = url
        self.url_list = set()

    def get_page_source(self):
        '''
        获取html文本
        '''
        self.driver.get(self.peopple_url)
        return self.driver.page_source

    def parse_user_html(self):
        '''
        解析用户动态
        '''
        soup = to_soup(self.get_page_source())
        
