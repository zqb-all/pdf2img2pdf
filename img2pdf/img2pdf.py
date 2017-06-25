#!/usr/bin/env python
#coding=utf-8
# -------------------------------------------------------------------------------
# Name:         PTools
# Purpose:      change PDF
#
# Author:       Liu.Qi
#
# Created:      20/10/2016
# Copyright:    (c) Chengdu Gerdige Technology Co., Ltd.
# -------------------------------------------------------------------------------

from __future__ import division

import os

from reportlab.platypus import SimpleDocTemplate,Image, PageBreak
from reportlab.lib.pagesizes import A4, landscape

import time
import math
import sys

from PIL import Image as pilImage
import re
import argparse

re_digits = re.compile(r'(\d+)')
def embedded_numbers(s):
     pieces = re_digits.split(s)               # 切成数字与非数
     pieces[1::2] = map(int, pieces[1::2])     # 将数字部分转成整数
     return pieces

def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
                            '=' * int(math.floor(cur * 50 / total)),
                            percent))
    sys.stdout.flush()


def GreentheImage(img_path):
    print("processing %s"% img_path)
    begin_time=time.clock()
    im = pilImage.open(img_path).convert("RGB")
    w, h = im.size
    print("w:%d,h:%d" % (w,h))
    for j in range(0,h):
        progressbar(j+1, h)
        for i in range(0,w):
            r,g,b=im.getpixel((i,j))
            if (r > 245 and g > 245 and b > 245):
                #print ("get pix i:%d,j:%d rgb:%d %d %d"%(i,j,r,g,b) )
                r = 199
                g = 237
                b = 204
                im.putpixel((i,j), (r,g,b))
    im.save(img_path)
    im.close()
    end_time=time.clock()
    print("done:%d"%(end_time - begin_time))



class Convert2PDF:

    # 支持的类型
    Const_Image_Format = [".jpg", ".jpeg", ".bmp", ".png"]

    # 获取的文件夹
    dirs = {}

    # a4的高宽
    a4_w, a4_h = landscape(A4)

    rootDir = ""

    def __init__(self,dirPath,bookname="default.pdf"):
        # 默认路径
        self.rootDir = dirPath
        self.bookname = bookname
        print('dirpath %s' % dirPath)
        self.begin()

    # 开始解析
    def begin(self):
        for parent, dirnames, filenames in os.walk(self.rootDir):
     #       for dirname in dirnames:
            dirname = self.rootDir
            dirData ={"name":"","pages":[],"isBook":False}
            dirName = dirname.split('/')[-2]
            dirData['name'] = dirName
            print('add dirName %s'%dirName)
            self.dirs[dirName] = dirData

            # 查找有无图片
            for filename in filenames:

                real_filename = os.path.join(parent, filename)
                # 取父文件夹名称为书名
                parentDirName = real_filename.split('/')[-2]

                if parentDirName in self.dirs.keys():
                    dirJsonData = self.dirs[parentDirName]
                else:
                    print('parentDirName %s not key'%parentDirName)
                    continue

                # 检查是否图片
                if real_filename and (os.path.splitext(real_filename)[1] in self.Const_Image_Format):
                    # 将图片添加至书本
                    print("real_filename:%s" % (real_filename))
                    dirJsonData['pages'].append(real_filename)

                    # 如果该书的isbook 是false 改为true
                    if not dirJsonData['isBook'] :
                        dirJsonData['isBook'] = True

        index = 1
        for dirName in self.dirs.keys():

            dirData = self.dirs[dirName]

            if dirData['isBook']:
                print("[*][转换PDF] : 开始. [名称] > [%s]" % (dirName))
                beginTime = time.clock()
                self.convert(dirData)
                endTime = time.clock()
                print("[*][转换PDF] : 结束. [名称] > [%s] , 耗时 %f s " % (dirName,(endTime-beginTime)))
                index += 1

        print("[*][所有转换完成] : 本次转换检索目录数 %d 个，共转换的PDF %d 本 " % (len(self.dirs),index-1))

    #
    # 开始转换
    #
    def convert(self,book):
        bookName = self.bookname
    #    bookName = self.rootDir + book['name'] + ".pdf"
        bookPages = book['pages']

        bookPagesData = []

        bookDoc = SimpleDocTemplate(bookName, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        #按文件名最后的数字顺序排序
        bookPages.sort(key=embedded_numbers)

        for bookPage in bookPages:

            img_w , img_h = ImageTools().getImageSize(bookPage)

            if self.a4_w / img_w < self.a4_h / img_h:
                ratio = self.a4_w / img_w
            else:
                ratio = self.a4_h / img_h
            #替换白色为绿色
            #GreentheImage(bookPage)
            data = Image(bookPage, img_w * ratio, img_h * ratio)
            bookPagesData.append(data)
            bookPagesData.append(PageBreak())

        try:
            bookDoc.build(bookPagesData)
            #print("已转换 >>>> " + bookName)
        except Exception as err:
            print("[*][转换PDF] : 错误. [名称] > [%s]" % (bookName))
            print("[*] Exception >>>> ",err)

class ImageTools :

    def getImageSize(self,imagePath):
        img = pilImage.open(imagePath)
        return img.size


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' ,'--input-dir' ,dest='dir_in' ,help="imgs to handle"   ,default='./')
    parser.add_argument('-o' ,'--output-pdf' ,dest='pdf_out' ,help="pdf to output"   ,default='default.pdf')
    args = parser.parse_args()
    Convert2PDF(args.dir_in,args.pdf_out)


