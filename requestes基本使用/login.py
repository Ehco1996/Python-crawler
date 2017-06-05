import requests
import bs4
import os
from PIL import Image


def get_post_data(url):

    # 首先获取到登录界面的html
    html = requests.get(url
                        )

    soup = bs4.BeautifulSoup(html.text, 'lxml')

    # 找到form的验证参数
    __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    

    # 下载验证码图片
    pic = requests.get(
        'http://jw.***.edu.cn/(gxv2le55n4jswm45mkv14o2n)/CheckCode.aspx').content
    with open('ver_pic.png', 'wb') as f:
        f.write(pic)

    # 打开验证码图片
    image = Image.open('{}/ver_pic.png'.format(os.getcwd()))
    image.show()

    # 构造需要post的参数表
    data = {'txtUserName': '',
            'Textbox1': '',
            'TextBox2': '',
            'txtSecretCode': "",
            '__VIEWSTATE': '',
            # 这里我将radio栏--学生 encode成gbk编码，以符合数据的要求
            'RadioButtonList1': '\xd1\xa7\xc9\xfa',
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': '', }

    # 构造登录的post参数
    data['__VIEWSTATE'] = __VIEWSTATE
    data['txtSecretCode'] = input('请输入图片中的验证码')
    data['txtUserName'] = input("请输入学号")
    data['TextBox2'] = input("请输入密码")

    return data


# 登录教务系统
def login(url,data):
    # 通过requests库构造一个浏览器session，这能帮我们自动、持久的管理cookies，
    s = requests.session()
    s.post(url, data=data)
    return s



base_url = 'http://jw.****.edu.cn/(gxv2le55n4jswm45mkv14o2n)/default2.aspx'
data = get_post_data(base_url)
print(data)
# 模拟登录教务系统
brow = login(base_url,data)

test = brow.get(
    'http://jw.****.edu.cn/(gxv2le55n4jswm45mkv14o2n)/xs_main.aspx?xh=14200406101')

# 测试看看是否能找到登陆后的信息
soup = bs4.BeautifulSoup(test.text, 'lxml')
try:
    name = soup.find('span', attrs={'id': 'xhxm'}).text
except:
    name = '登录失败 '

print(name)

