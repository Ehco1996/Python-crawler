'''
测试selenium模拟浏览器
和phantomjs无页面浏览器

导出PhantomJs浏览器帮助文档
'''

from selenium import webdriver
import sys

browser = webdriver.PhantomJS()
out = sys.stdout

sys.stdout = open('browserHelp.txt','w')
help(browser)
sys.stdout.close()
sys.stdout = out
browser.quit()
exit()