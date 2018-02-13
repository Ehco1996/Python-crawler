from bs4 import BeautifulSoup


def to_soup(page):
    return BeautifulSoup(page, 'lxml')


with open('1.html', 'r') as f:
    html = f.read()


soup = to_soup(html)

res = soup.find_all('div', class_="List-item")
for item in res:
    ele = item.find('h2', class_='ContentItem-title')
    title = ele.text
    url = 'https://www.zhihu.com' + ele.a['href']
    print(title, url)
