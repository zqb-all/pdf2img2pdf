#!/usr/bin/env python
#coding: utf-8


import sys
import os

from img2pdf.img2pdf import Convert2PDF
from pdf2img.pdf2img import Pdf2img

from imgchangecolor.imgchangecolor import ChangeColor
#log = LoggerHandler.getLogger("main")

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i' ,'--input'      ,dest='pdf_in' ,help="pdf to handle", default='demo.pdf')
parser.add_argument('-o' ,'--output'     ,dest='pdf_out',help="image after handle", default='./')
parser.add_argument('-rs','--red-start'  ,dest='red_s'  ,help="red start"         ,type=int, default=245)
parser.add_argument('-gs','--green-start',dest='green_s',help="green start"       ,type=int, default=245)
parser.add_argument('-bs','--blue-start' ,dest='blue_s' ,help="blue start"        ,type=int, default=245)
parser.add_argument('-re','--red-end'    ,dest='red_e'  ,help="red end"           ,type=int, default=255)
parser.add_argument('-ge','--green-end'  ,dest='green_e',help="green end"         ,type=int, default=255)
parser.add_argument('-be','--blue-end'   ,dest='blue_e' ,help="blue end"          ,type=int, default=255)
parser.add_argument('-rn','--red-new'    ,dest='red_n'  ,help="red new"           ,type=int, default=199)
parser.add_argument('-gn','--green-new'  ,dest='green_n',help="green new"         ,type=int, default=237)
parser.add_argument('-bn','--blue-new'   ,dest='blue_n' ,help="blue new"          ,type=int, default=204)
args = parser.parse_args()

pdf_to_handle = args.pdf_in
pdf_out = args.pdf_out
pdf_path=os.path.split(pdf_to_handle)[0]

Pdf2img(pdf_to_handle)

Const_Image_Format = [".jpg", ".jpeg", ".bmp", ".png"]

for parent, dirnames, filenames in os.walk(pdf_path):
    for filename in filenames:
            real_filename = os.path.join(parent, filename)
            print("real_filename:%s"%real_filename)
            if real_filename and (os.path.splitext(real_filename)[1] in Const_Image_Format):
                ChangeColor(real_filename,real_filename,args.red_s,args.red_e,args.green_s,args.green_e,args.blue_s,args.blue_e,args.red_n,args.green_n,args.blue_n)

Convert2PDF(pdf_path,pdf_out)

