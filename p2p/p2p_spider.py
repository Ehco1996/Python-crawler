'''
爬取P2p 网贷之家的各项数据
    列表页：http://www.wdzj.com/dangan/
    详情页：http://www.wdzj.com/dangan/(keyword)/

公司要求使用lxml，在某种数量级的情况下，soup库太慢了
'''


import requests
import time
import json
from lxml import etree
from lxml.html import fromstring


def json_extractor(html, currPage):
    """
    解析P2P页面的列表页
    Args:
        json 数据 字典格式返回
    Returns:
        数组: 每条为一个完整记录，记录由字典格式保存
    """
    results = list()
    json = eval(html)
    try:
        info_list = json['list']
        for info in info_list:
            title = info['platName']
            # 平均收益
            platEarnings = info.get('platEarnings', -1)
            # 参考投资期限
            term = info.get('term', -1)
            # 上线时间
            onlineDate = info.get('onlineDate', -1)
            # 注册资本
            registeredCapital = info.get('registeredCapital', -1)
            # 注册地
            cityName = info.get('cityName', -1)
            # 详细页面的url
            url = 'http://www.wdzj.com/dangan/{}/'.format(
                info['platNamePin'])
            result = {
                'title': title,
                'platEarnings': platEarnings,
                'term': term,
                'onlineDate': onlineDate,
                'cityName': cityName,
                'url': url,
                'registeredCapital': registeredCapital,
            }
            results.append(result)
        return results
    except:
        # print('第{}页解析错误'.format(currPage))
        return -1


def detail_extractor(text, info):
    '''
    解析P2P页面的列表页
    Args:
        text 网页文本文件
        info 数据 字典格式 记录列表页面解析的信息
    Returns:
        数组: 每条为一个完整记录，记录由字典格式保存
    '''
    results = list()

    print('开始解析详情界面{}'.format(info['url']))
    # tree = etree.HTML(text)
    tree = fromstring(text, "ignore")

    # 平均参考收益率
    income_rate = tree.xpath(
        '/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/dl/dd[1]/em/text()')[0]
    # 参考投资期限
    loan_period = tree.xpath(
        '/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/dl/dd[2]/em/text()')[0]
    # 成交量（万元）
    amount = tree.xpath(
        '/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/dl/dd[3]/em[1]/text()')[0]
    # 投资人数
    bidder_num = tree.xpath(
        '/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/dl/dd[4]/em[1]/text()')[0]
    # 借款人数
    borrower_num = tree.xpath(
        '/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/dl/dd[5]/em[1]/text()')[0]
    # 日资金净流入（万元）
    net_inflow = tree.xpath(
        '/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/dl/dd[6]/em[1]/text()')[0]
    # 日待还余额（万元）
    money_stock = tree.xpath(
        '/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/dl/dd[7]/em[1]/text()')[0]
    # 银行存管
    bankCapital = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[1]/dd[2]/div[2]/text()')[0].strip()
    # 融资记录
    riskcontrolDetail = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[1]/dd[3]/div[2]/text()')[0].strip()
    # 监管协会
    regulatoryAssociation = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[1]/dd[4]/div[2]/text()')[0].strip()
    # ICP号
    recordLicId = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[1]/dd[5]/div[2]/text()')[0].strip()
    # 自动投标
    autoBid = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[2]/dd[1]/div[2]/text()')[0].strip()
    # 债权转让
    newTrustCreditor = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[2]/dd[2]/div[2]/text()')[0].strip()
    # 投标保障
    bidSecurity = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[2]/dd[3]/div[2]/text()')[0].strip()
    # 保障模式
    securityModel = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[2]/dd[4]/div[2]/text()')[0].strip()
    # 担保机构
    gruarantee = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[2]/dd[5]/div[2]/text()')[0].strip()
    # 风险准备金存管
    riskDepository = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[1]/dl[2]/dd[5]/div[2]')[0].xpath('string(.)').strip()
    # 公司简介,分段操作，去除空格
    raw_info = tree.xpath(
        '/html/body/div[8]/div/div[1]/div[2]/div[2]/div[1]/div/div')[0].xpath('string(.)').strip()
    companyInfo = ''.join(raw_info.split())
    result = {
        'income_rate': income_rate,
        'loan_period': loan_period,
        'loan_period': loan_period,
        'amount': amount,
        'bidder_num': bidder_num,
        'borrower_num': borrower_num,
        'net_inflow': net_inflow,
        'money_stock': money_stock,
        'bankCapital': bankCapital,
        'riskcontrolDetail': riskcontrolDetail,
        'regulatoryAssociation': regulatoryAssociation,
        'recordLicId': recordLicId,
        'autoBid': autoBid,
        'newTrustCreditor': newTrustCreditor,
        'bidSecurity': bidSecurity,
        'securityModel': securityModel,
        'gruarantee': gruarantee,
        'riskDepository': riskDepository,
        'companyInfo': companyInfo,
    }
    result.update(info)
    results.append(result)
    return results


def write_to_json(data, name):
    with open('json/{}.json'.format(name), 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def write_to_data(data, name):
    with open('data/{}.json'.format(name), 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def get_json_data(currPage):
    data = {
        'sort': 0,
        'currPage': 1,
    }
    request_url = 'http://www.wdzj.com/front_select-plat'
    data['currPage'] = int(currPage)
    try:
        r = requests.post(request_url, headers=header, data=data)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        write_to_json(r.json(), data['currPage'])
        print('第{}页数据下载完毕'.format(data['currPage']))
    except:
        print('{}页数据下载失败！')
        return -1


# # 解析数据
def deal_list_response():
    for i in range(1, 223):
        with open('json/{}.json'.format(i), 'r') as f:
            data = f.read()
            ext_data = json_extractor(data, i)
            if ext_data == -1:
                print('第{}页解析错误'.format(i))
            else:
                write_to_data(ext_data, i)


def get_html_text(url):
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return -1


# 测试部分
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

# 下载所有的原始数据
# for i in range(1, 223):
#     time.sleep(1)
#     get_json_data(i)

# 测试爬取详情页
# 测试抓取第22页的详情数据
with open('data/22.json', 'r') as f:
    info_list = eval(f.read())
    for info in info_list:
        time.sleep(1)
        html = get_html_text(info['url'])
        if html != -1:
            ext_data = detail_extractor(html, info)
            print(ext_data)
        else:
            print('{}页解析下载失败'.format(info['url']))
