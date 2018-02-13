from lazyspider.lazyheaders import LazyHeaders

# 登录之后的curl字符串
CURL = ''''''
# 轮子哥的主页地址
VZCH = 'https://www.zhihu.com/people/excited-vczh/activities'

# 获取你的cookie和headers
lz = LazyHeaders(CURL)
COOKIES = lz.getCookies()
HEDADERS = lz.getHeaders()
# print(COOKIES, HEDADERS)
