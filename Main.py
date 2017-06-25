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
                ChangeColor(real_filename,real_filename)

Convert2PDF(pdf_path,pdf_out)

