
# 导入对数据库操作的封装和配置文件
from stroe import DbToMysql
import config

# 初始化组件
store = DbToMysql(config.EHCO_DB)

# 数据查询
res = store.find_by_sort('DoubanTop250', 'ranking', 10, 'ASC')

for data in res:
    print(data['name'])
