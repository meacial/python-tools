#!/usr/local/bin/python2
#encoding=utf-8
"""
切分图片
"""
import os
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


label_image_path='/Users/lgp/project/python/com.meacial/12306/label_image/'
cuted_image='/Users/lgp/project/python/com.meacial/12306/cuted_image/'

image_path = '/Users/lgp/project/python/com.meacial/12306/login_captcha_image'

def cut_and_save_label(img,filename):
    temp = filename.split('.')
    filename = temp[0]+'_label.'+temp[1]
    label_region = (0, 1, 293,30)
    cutimg = img.crop(label_region)
    cutimg.save(label_image_path+filename)


def cut_and_save_img(img,filename):
    temp = filename.split('.')
    x_start = 5  # 第一张图片的起始x坐标
    y_start = 41 # 第一张图片的起始y坐标
    between = 6  # 每个图片之间的间隔
    side = 66  # 图片边长，正方形
    for y,x in ((y,x) for y in (0,1) for x in (0,1,2,3)):
        x1 = x_start + x * side + x * between
        x2 = x1 + side
        y1 = y_start + y * side + y * between
        y2 = y1 + side
        regoin = (x1,y1,x2,y2)  # x1,y1,x2,y2
        cutimg = img.crop(regoin)

        cut_filename = temp[0]+str(y*4 + x)+'.'+temp[1]
        cutimg.save(cuted_image+cut_filename)


def read_img(imgfile):
    return Image.open(imgfile)


if __name__ == '__main__':
    for root,dirs,files in os.walk(image_path):
        for f in files:
            print root+'/'+f
            try:
                img = read_img(root+"/"+f)
                cut_and_save_label(img, f)
                cut_and_save_img(img,f)
                img.close()
            except Exception as ex:
                print ex
