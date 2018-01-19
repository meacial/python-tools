#coding:utf-8
#Test one page
import pytesseract
from PIL import Image

"""

https://www.jianshu.com/p/c52e39053dcf
"""

def processImage():
    image = Image.open('20180110103829_label.jpg')

    #背景色处理，可有可无
    image = image.point(lambda x: 0 if x < 143 else 255)
    newFilePath = 'raw-test.png'
    image.save(newFilePath)

    content = pytesseract.image_to_string(Image.open(newFilePath), lang='chi_sim')
    #中文图片的话，是lang='chi_sim'
    print(content)

processImage()
