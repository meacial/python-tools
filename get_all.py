#!/usr/local/bin/python2
#encoding=utf-8
"""
爬取网页所有的js,css,html等信息
"""
import urllib
import requests
import random
import os
import sys
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding( "utf-8" )

session = requests.Session()



login_headers = {
        "Host": "kyfw.12306.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
        }

logined_headers = login_headers.copy()
logined_headers['Referer']='https://kyfw.12306.cn/otn/leftTicket/init'


host = "http://www.12306.cn"

# 页面初始化，获取cookie等信息
def index_request():
    response = session.get('https://kyfw.12306.cn/otn/leftTicket/init',headers=login_headers)
    cookie  = ''
    for key,value in response.cookies.items():
        cookie += key+'='+value+';'
    cookie = cookie[0:-1]
    logined_headers['Cookie']=cookie
    return response.text


# 解析网页
def login_page_parser(html):
    soup = BeautifulSoup(html)
    urllist = []
    scriptlist = soup.findAll('script')
    for script in scriptlist:
        if script.get('src'):
            urllist.append(script.get('src'))

    return urllist


def get_all(urllist):
    for url in urllist:
        response = session.get(host+url, headers=logined_headers)
        print response.text
        filename = url.split('/')[-1:][0]
        filename = filename.split('?')[0:1][0]
        with open(filename, 'w') as f:
            f.write(response.text)


def usercheck():
    url = 'https://kyfw.12306.cn/otn/login/checkUser'
    response =  session.get(url)
    print response.text
    print response.content

def get_login_image():
    url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
    response = session.get(url)

    for k,v in response.cookies.items():
        print k , ' = ', v
        logined_headers['Cookie']  = logined_headers['Cookie'] + ';'+ k +'='+v

    with open('login.jpg', 'wb') as img:
        img.write(response.content)



def get_point(index):
    '''
    根据图片的index，返回图片的坐标
    '''
    point_str = ''
    for i in index:
        if i == 1:
            point_str += ',39,36'
        elif i == 2:
            point_str += ',120,41'
        elif i == 3:
            point_str += ',185,44'
        elif i == 4:
            point_str += ',244,46'
        elif i == 5:
            point_str += ',38,112'
        elif i == 6:
            point_str += ',110,118'
        elif i == 7:
            point_str += ',185,123'
        elif i == 8:
            point_str += ',259,119'
    return point_str[1:]



def image_check():
    import json
    # 图片验证码验证
    url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    answer = input('依次输入图片的x,y坐标:')
    data = {
        'answer': answer,
        'login_site': 'E',
        'rand': 'sjrand',
        '_json_att':''
    }
    print logined_headers
    response = session.post(url,headers=logined_headers, data=json.dumps(data))
    print response.text
    print response.content


if __name__ == '__main__':
    #get_all('https://kyfw.12306.cn/otn/login/init')
    #get_response_info('https://kyfw.12306.cn/otn/login/init')
    #index_request()
    html = index_request()
    #urllist = login_page_parser(html)
    #get_all(urllist)
    #for url in urllist:
    #    print url

    import time
    import json

    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #print today

    day = '2018-02-12'

    qryTicketUrl = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date='+day+'&leftTicketDTO.from_station=BXP&leftTicketDTO.to_station=XAY&purpose_codes=ADULT'

    data = session.get(qryTicketUrl).content
    #print data

    json1 = json.loads(data)
    #print json1

    for record in json1['data']['result']:
        #print record
        pass


    usercheck()
    get_login_image()
    image_check()
