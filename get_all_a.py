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
import time
import json

from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding( "utf-8" )


session = requests.Session()

host = "http://www.12306.cn"

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



headers = {}
cookies = {}


def update_headers():
    cookie_str = ''
    for k,v in cookies.items():
        cookie_str += k+'='+v+';'
    headers['Cookie'] = cookie_str[:-1]



# 页面初始化，获取cookie等信息
def index_request():
    response = session.get('https://kyfw.12306.cn/otn/leftTicket/init',headers=login_headers)
    cookie  = ''
    for key,value in response.cookies.items():
        cookie += key+'='+value+';'
    cookie = cookie[0:-1]
    logined_headers['Cookie']=cookie
    return response.text


def usercheck():
    url = 'https://kyfw.12306.cn/otn/login/checkUser'
    response =  session.get(url)
    print response.text
    print response.content


def get_login_image():
    '''
    获取图片验证码，并保存相关的session信息
    '''
    url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
    response = session.get(url)
    for k,v in response.cookies.items():
        cookies[k] = v
    # 将获取的验证码保存到本地
    with open('login.jpg', 'wb') as img:
        img.write(response.content)


    #print response.text
    #print response.content
    for head in response.headers:
        print head, ' = ' , response.headers[head]
    print cookies

def get_point(index):
    '''
    根据图片的index，返回图片的坐标
    '''
    point_str = ''
    for n in range(len(index)):
        i = index[n]
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



def image_check(answer):
    import json
    # 图片验证码验证
    url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    data = {
        'answer': answer,
        'login_site': 'E',
        'rand': 'sjrand'
    }
    update_headers()

    #print headers
    #print data


    tmpheader = {}
    tmpheader['Accept']='application/json, text/javascript, */*; q=0.01'
    tmpheader['Accept-Encoding']='gzip, deflate, br'
    tmpheader['Accept-Language']='zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    tmpheader['Cache-Control']='no-cache'
    tmpheader['Connection']='keep-alive'
    tmpheader['Cookie']='_passport_session=2530b74681fa4987b98f0413e1ed26416170; _passport_ct=c1547e2dd3e84139adcbe1dabe2d9a12t0904; RAIL_EXPIRATION=1516050303514; RAIL_DEVICEID=Gnaug_OHb6p_G_Qp3wJxgNKp4WkMftPSPbDfnhvXSjV5nuHq2iyNKOXNHKQze2fcBsI0vwM6zxGam7p0ak926yyYFNC4XIS7zq2yhP4HIMkOyHhGkPQSMkqG1c-IHu0_1CdNQijYrBst7GkYIte3UKdjDsGMUxC-; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=451150346.64545.0000; BIGipServerpool_passport=401408522.50215.0000'
    tmpheader['Host']='kyfw.12306.cn'
    tmpheader['Referer']='https://kyfw.12306.cn/otn/login/init'
    tmpheader['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
    tmpheader['X-Requested-With']='XMLHttpRequest'


    print tmpheader
    print json.dumps(data)

    tmpcookies = {}
    tmpcookies['_passport_session']='2530b74681fa4987b98f0413e1ed26416170'
    tmpcookies['_passport_ct']='c1547e2dd3e84139adcbe1dabe2d9a12t0904'
    tmpcookies['RAIL_EXPIRATION']='1516050303514'
    tmpcookies['RAIL_DEVICEID']='Gnaug_OHb6p_G_Qp3wJxgNKp4WkMftPSPbDfnhvXSjV5nuHq2iyNKOXNHKQze2fcBsI0vwM6zxGam7p0ak926yyYFNC4XIS7zq2yhP4HIMkOyHhGkPQSMkqG1c-IHu0_1CdNQijYrBst7GkYIte3UKdjDsGMUxC-'
    tmpcookies['route']='9036359bb8a8a461c164a04f8f50b252'
    tmpcookies['BIGipServerotn'] = '451150346.64545.0000'
    tmpcookies['BIGipServerpool_passport'] = '401408522.50215.0000'

    response = requests.post(url,json=json.dumps(data),cookies=tmpcookies,headers=tmpheader)
    print response.text
    print response.content



if __name__ == '__main__':

    get_login_image()

    input_point = input('输入图片验证码的序号（1-8，逗号风格：')

    answer = get_point(input_point)

    image_check(answer)

