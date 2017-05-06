'''
爬取Dota菠菜结果信息
使用 requests --- bs4 线路
Python版本： 3.6
OS： mac os 12.12.4
'''

import requests
import bs4

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return " ERROR "

def print_result(url):
    '''
    查询比赛结果，并格式化输出！
    '''
    html = get_html(url)
    soup =  bs4.BeautifulSoup(html,'lxml')
    match_list = soup.find_all('div', attrs={'class': 'matchmain bisai_qukuai'})
    for match in match_list:
        time = match.find('div', attrs={'class': 'whenm'}).text.strip()
        teamname = match.find_all('span', attrs={'class': 'team_name'})
       
        
        #由于网站的构造问题，队名有的时候会不显示，所以我们需要过滤掉一些注释,方法如下:
        if teamname[0].string[0:3] == 'php':
            team1_name = "暂无队名"
        else:
            team1_name = teamname[0].string
        
        # 这里我们采用了css选择器：比原来的属性选择更加方便
        team1_support_level = match.find('span', class_='team_number_green').string

        team2_name = teamname[1].string
        team2_support_level = match.find('span', class_='team_number_red').string

        print('比赛时间：{}，\n 队伍一：{}      胜率 {}\n 队伍二：{}      胜率 {} \n'.format(time,team1_name,team1_support_level,team2_name,team2_support_level))



def main():
    url= 'http://dota2bocai.com/match'
    print_result(url)

if __name__ == '__main__':
    main()