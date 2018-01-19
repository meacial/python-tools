#!/usr/local/bin/python2.7
# -*- encoding:utf-8 -*-

import chardet
from sys import argv
def detect_file_encoding(file_path):
    ''' 返回文件的编码 '''
    f = open(file_path, 'r')
    data = f.read()
    predict =  chardet.detect(data)
    f.close()
    return predict['encoding']

if __name__ == '__main__':
    # file_path = '/Users/lgp/20180915/D7/MD_痛风.txt'
    _,file_path = argv
    print detect_file_encoding(file_path)
