'''
通过一些小例子来了解bs4库的基本使用，
本篇为lxml解析器的使用
解析的html为当前目录下的demo.html
'''
import bs4


#首先我们先将html文件已lxml的方式做成一锅汤
soup = bs4.BeautifulSoup(open('Beautiful Soup 爬虫/demo.html'),'lxml')

#我们把结果输出一下，是一个很清晰的树形结构。
#print(soup.prettify())

'''
OUT:

<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
  </p>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link3">
    Tillie
   </a>
   ;
and they lived at the bottom of a well.
  </p>
  <p class="story">
   ...
  </p>
 </body>
</html>
'''