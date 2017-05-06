import requests
import bs4
import re

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        print(r.apparent_encoding)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Someting Wrong！"


def get_txt_url(url):
    '''
    获取该小说每个章节的url地址：

    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1').text
    with open('/Users/ehco/Documents/codestuff/Python-crawler/小说/{}.txt'.format(txt_name),"a+") as f:
      f.write('小说标题：{} \n'.format(txt_name))
    for url in lista:
        url_list.append('http://www.qu.la/' + url.a['href'])

    
    return url_list,txt_name



url = 'http://www.qu.la/book/28888/'

def get_one_txt(url,txt_name):
  html = get_html(url).replace('<br/>','\n')  
  soup = bs4.BeautifulSoup(html,'lxml')
  try:
    txt  = soup.find('div',id='content').text.replace('chaptererror();','')
    title = soup.find('title').text
  
    with open('/Users/ehco/Documents/codestuff/Python-crawler/小说/{}.txt'.format(txt_name),"a") as f:
      f.write(title+'\n\n')
      f.write(txt)
      print('当前章节{} 已经下载完毕'.format(title))
  except:
    print('someting wrong')



a=[1,2,3,4,5]
for i in a:
  print(a.index(i)/len(a)*100)