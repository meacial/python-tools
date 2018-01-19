#!/usr/local/bin/python2
#encoding=utf-8
"""
获取登录图片验证码
"""
import datetime
import requests
import time
url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.29713125124634776'

def download_image(outputdir):
    """
    下载保存图片
    """
    response = requests.get(url)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open(outputdir+'/'+filename+'.jpg', 'wb') as imagefile:
        imagefile.write(response.content)


if __name__ == '__main__':
    for i in range(10000):
        download_image('login_captcha_image')
        time.sleep(1)




