#!/usr/local/bin/python2
#encoding=utf-8

"""

读取MongoDB中Disease2Xuewei，中的穴位数据，并查找对应的图片信息，将疾病穴位图片信息，保存到diseaseToxuewei表中

"""
# 修改默认编码
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import base64

import pymongo

conn = pymongo.MongoClient(host="10.117.130.194",port=27017)

cisai_db = conn['cis-ai']
cisaidyl_db = conn['cis-ai-dyl']

# print cisai_db.diseaseToxuewei.find_one({'diseases':'急性上呼吸道感染'})



class disease2xueweiOne():
    pass



import os

image_path = '/Users/lgp/project/python/com.meacial/rentixuewei/image3'

image_label_path = {}

for (root, dirs, files) in os.walk(image_path):
    for filename in files:
        image_label_path[filename] = '%s/%s' % (root, filename)


def get_image_by_xuewei(xuewei):
    for k,v in image_label_path.items():
        if xuewei in k:
            return v
    return None



if __name__ == '__main__':
    cisaidyl_db.diseaseToxuewei.drop()
    for item in cisai_db.Disease2Xuewei.find():
        disease = item['disease']
        xueweilist = item['xuewei']
        scorelist = item['score']

        for i in range(len(xueweilist)):
            xuewei = xueweilist[i]
            score = scorelist[i]
            image_file = get_image_by_xuewei(xuewei)
            image_base64_str = ''
            if image_file is not None:
                with open(image_file,'rb') as f:
                    image_base64_str = 'data:image/jpeg;base64,'+base64.b64encode(f.read())

            xueweiinfo = cisai_db.Xuewei2Disease.find_one({'xuewei':xuewei})
            position = xueweiinfo['position']
            cur = ''
            if 'cur' in xueweiinfo:
                cur = xueweiinfo['cur']
            cisaidyl_db.diseaseToxuewei.save({'diseases':disease, 'xuewei': xuewei, 'position': position, 'cur': cur, 'score': score, 'pic': image_base64_str})

