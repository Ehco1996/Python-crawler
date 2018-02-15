import os
from lazyspider.lazystore import LazyMysql

from parse import parse_activities
from configs import LOCAL_DB, USER_SIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def json_to_db():
    '''
    json->mysql
    '''
    store = LazyMysql(LOCAL_DB)
    for file in os.listdir(BASE_DIR+'/data/'):
        file_abs_path = BASE_DIR+'/data/'+file
        # 解析json格式的文件，筛选我们要的数据
        res = parse_activities(file_abs_path)
        for data in res:
            try:
                data.update({'username': USER_SIG})
                store.save_one_data(data, 'zhihu_activities')
            except:
                print('error !!!!!!!!!')
        print('所有文件导入完毕')
        

if __name__ == '__main__':
    json_to_db()
