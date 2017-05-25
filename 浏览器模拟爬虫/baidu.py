'''
使用Selenium模拟浏览器
抓取百度查询结果
'''

# 导入selenium模块中的web引擎
from selenium import webdriver


# 建立浏览器对象 ，通过Phantomjs
browser = webdriver.PhantomJS()

# 设置访问的url
url = 'https://www.baidu.com'

# 访问url
browser.get(url)

# 等待一定时间，让js脚本加载完毕
browser.implicitly_wait(3)

# 找到搜索框
text = browser.find_element_by_id('kw')

# 清空搜索框的文字
text.clear()

# 填写搜索框的文字
text.send_keys('python')

# 找到submit按钮
button = browser.find_element_by_id('su')

# 点击按钮 提交搜索请求
button.submit()


# 查看当前浏览器标题
print(browser.title)

# 以截图的方式查看浏览器的页面
browser.save_screenshot('text.png')

# 找到结果 结果保存为列表变量
results = browser.find_elements_by_class_name('t')

# 循环遍历找出每个结果的标题和url
for result in results:
    print('标题：{} 超链接：{}'.format(result.text,
                                result.find_element_by_tag_name('a').get_attribute('href')))
