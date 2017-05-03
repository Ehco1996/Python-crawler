'''
通过Python来学习re库 --- 正则表达式相关内容

'''

import re

test = 'python is the best language , pretty good !'

p = re.findall('p+',test)

print(p)


'''
re.search(pattern, string, flags=0) 
在一个字符串中搜索匹配正则表达式的第一个位置
返回match对象
∙ pattern : 正则表达式的字符串或原生字符串表示 
∙ string : 待匹配字符串
∙ flags : 正则表达式使用时的控制标记
'''

str1 = 'hello , world ,life is short ,use Python .WHAT? '

a = re.search(r'\w+',str1)
print(a.group())    #  hello

b = re.search(r'w.+D',str1,re.I)
print(b.group())


'''
re.findall(pattern, string, flags=0) 
搜索字符串，以列表类型返回全部能匹配的子串
∙ pattern : 正则表达式的字符串或原生字符串表示 
∙ string : 待匹配字符串
∙ flags : 正则表达式使用时的控制标记
'''

c = re.findall(r'\w+',str1)
print (c)
#['hello', 'world', 'life', 'is', 'short', 'use', 'Python', 'WHAT']

str2 = 'hssso'
re1 = re.compile(r'h.{3}o')
print(re1.findall(str1))
print(re1.findall(str2))
# ['hello']
#['hssso']

'''
match 对象的属性

.string : 待匹配的文本 
.re     : 匹配时使用的patter对象(正则表达式)
.pos    : 正则表达式搜索文本的开始位置
.endpos : 正则表达式搜索文本的结束位置   
'''
d = re.search(r'e.+d',str1)
print(d.group()) # ello , world
print (d.string) # hello , world ,life is short ,use Python .WHAT?
print (d.re) # re.compile('e.+d')
print (d.pos) # 0
print (d.endpos) # 48
