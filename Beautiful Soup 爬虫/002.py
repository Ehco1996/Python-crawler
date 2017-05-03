'''
简单的bs4库的使用
'''

import bs4


#首先我们先将html文件已lxml的方式做成一锅汤
soup = bs4.BeautifulSoup(open('Beautiful Soup 爬虫/demo.html'),'lxml')

#找到head标签里的内容
#print (soup.head)

#找到所有的text内容
#print (soup.text)

#找到第一个a标签
#print (soup.a)

#找到所有a标签
#print (soup.find_all('a'))

#找到a标签下的所有子节点，一列表方式返回
#print(soup.a.contents)

#通过.children生成器，我们可以循环迭代出每一个子节点
#tag = soup.body
#for s in tag.children:
#    print(s)

#通过迭代找到所的string
for i in soup.strings:
    print(i)