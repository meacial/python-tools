#!/usr/local/bin/python2
#encoding=utf-8
"""
图片切割
"""

from PIL import Image
filepath = '/Users/lgp/project/python/com.meacial/12306/login_captcha_image/20180110124029.jpg'
filepath='/Users/lgp/project/python/com.meacial/12306/login_captcha_image/20180110124217.jpg'
filepath='/Users/lgp/project/python/com.meacial/12306/login_captcha_image/20180110115744.jpg'
image = Image.open(filepath)

# 标题图片
reg = (120, 1, 293,30)
cutimg = image.crop(reg)
cutimg.save('20180110132604_0.jpg')

# 第一张图片
reg = (5, 41, 72,107)
cutimg = image.crop(reg)
cutimg.save('20180110132604_1.jpg')

# 第二张图片
reg = (78, 41, 143, 107)
cutimg = image.crop(reg)
cutimg.save('20180110132604_2.jpg')

# 第三张图片
reg = (149, 41, 215, 107)
cutimg = image.crop(reg)
cutimg.save('20180110132604_3.jpg')

# 第四张
reg = (221, 41, 287, 107)
cutimg = image.crop(reg)
cutimg.save('20180110132604_4.jpg')

# 第五张
reg = (5, 113, 72, 179)
cutimg = image.crop(reg)
cutimg.save('20180110132604_5.jpg')

# 第六张
reg = (78, 113, 143, 179)
cutimg = image.crop(reg)
cutimg.save('20180110132604_6.jpg')

# 第七张
reg = (149, 113, 215, 179)
cutimg = image.crop(reg)
cutimg.save('20180110132604_7.jpg')

# 第八张
reg = (221, 113, 287, 179)
cutimg = image.crop(reg)
cutimg.save('20180110132604_8.jpg')
