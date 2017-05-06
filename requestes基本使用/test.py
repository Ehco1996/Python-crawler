import bs4

html = '''
  <div class="matchmain bisai_qukuai"><!--比赛列表块 -->

           <div class="matchheader">

        <div class="whenm">
        比赛结束，&nbsp;&nbsp;比分：X：X，A队获胜。
        </div>
        <div class="whenm hui1" >
            CIS Carnage        </div>
    </div>

     <div class="match border1" style="background-image: url(../images/index/liansai/5600659cd4d08908f62fb8a9c0d30c8a.jpg)">
  <div class="matchleft">
    <a href="../match?m=1979">
    <div style="width: 36%; float: left; text-align: right">
      <div class="team" style="float: right; background: url('../images/index/ceshi/PR.jpg')"></div>
      <div class="teamtext"><span class="team_name">PR战队</span></div>
      <div class="clearfix"></div>
      <div class="zhichilv1"><span class="team_number_green">39%</span><br><span class="team_number_green">39%</span></div>
    </div>
    <div style="width: 28%; float: left; text-align: center; margin-top: 0.6em"><img src="../images/index/vs.png" width="31" height="30"><br>
    <div class="zhichi1">物品支持<br>积分支持</div>
    </div>
    <div style="width: 36%; float: left; text-align: left">
      <div class="team" style="float: left; background: url('../images/index/ceshi/Empire.jpg')"></div>
      <div class="teamtext"><span class="team_name">Empire</span></div>
       <div class="clearfix"></div>
      <div class="zhichilv2"><span class="team_number_red" style="color: #00ad00">61%</span><br><span class="team_number_red"  style="color: #00ad00">61%</span></div>
    </div>
    </a>
  </div>
</div>
'''

soup = bs4.BeautifulSoup(html, 'lxml')
match_list = soup.find_all('div', attrs={'class': 'matchmain bisai_qukuai'})
for match in match_list:
    time = match.find('div', attrs={'class': 'whenm'}).text.strip()
    teamname = soup.find_all('span', attrs={'class': 'team_name'})
    team1_name = teamname[0].string
    # 这里我们采用了css选择器：比原来的属性选择更加方便
    team1_support_level = soup.find('span', class_='team_number_green').string

    team2_name = teamname[1].string
    team2_support_level = soup.find('span', class_='team_number_red').string

str1 = 'pip3'

print(str1[0:2])