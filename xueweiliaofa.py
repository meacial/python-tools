#!/usr/local/bin/python2
#encoding=utf-8
'''
主页>中医疗法>穴位疗法
http://www.rentixuewei.com/html/zhongyiliaofa/xuewei/list_145_1.html
'''

import sys
from bs4 import BeautifulSoup
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

domain = 'http://www.rentixuewei.com'

pageurl_prefix = domain+'/html/zhongyiliaofa/xuewei/'

start_url = domain+'/html/zhongyiliaofa/xuewei/list_145_1.html'

queuelist = []

imageurldict = {}


def get_html(url):
    '''
    爬取网页
    '''
    response = requests.get(url)
    if response:
        response.encoding='gb2312'
        return response.text


def download(url, outputfile):
    '''
    下载图片并保存到本地
    '''
    response = requests.get(url)
    if response:
        with open(outputfile,'wb') as image:
            image.write(response.content)


def parser(html):
    '''
    解析网页，获取网页中的图片地址，和下一页的地址
    '''
    global queuelist
    soup = BeautifulSoup(html)
    for a in soup.select('.list_main_L_box > li > a'):
        if a.has_attr('href'):
            queuelist.append(a.get('href'))

    is_next_find = False
    next_url = None
    for page in soup.select('.dede_pages > ul > li'):
        if page.has_attr('class'):
            is_next_find = True
        else:
            if is_next_find:
                a = page.find('a')
                if a and a.has_attr('href'):
                    next_url = a.get('href')
                break
    return next_url


def parser_content(html):
    '''
    解析内容页面，获取图片地址
    '''
    soup = BeautifulSoup(html)
    for img in soup.select('.content2 > p > img'):
        if img and img.has_attr('src'):
            imageurldict[img.get('src')] = img.get('alt')


if __name__ == '__main__':
    import time
    next_url = start_url
    # 爬取所有页面列表
    while True:
        time.sleep(1)
        html = get_html(next_url)
        next_url = parser(html)
        if next_url:
            next_url = pageurl_prefix + next_url
        else:
            break
    # 解析所有页面中的图片地址
    for url in queuelist:
        html = get_html(domain + url)
        parser_content(html)

    # 下载图片并保存
    for (imageurl,xuewei) in imageurldict.items():
        filename = u'image/%s_%s' % (xuewei,imageurl.split('/')[-1:][0])
        download(domain+imageurl,filename)
        time.sleep(1)
