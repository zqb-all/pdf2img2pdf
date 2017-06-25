#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wand.image import Image
from PyPDF2 import PdfFileReader
import os
import warnings
import multiprocessing
import re
import argparse


def process(single_page):
    pattern = re.compile('\[|\]')
    # 页码
    page_num = pattern.split(single_page)[1]
    file_text = os.path.splitext(single_page)[0]
    with Image(filename=single_page, resolution=200) as converted:
        converted.compression_quality = 45
        newfilename = file_text + page_num + '.jpg'
        converted.save(filename=newfilename)
        print(multiprocessing.current_process().name + '' + newfilename)
    if not os.path.isfile(newfilename):
        print('page of file is not found:[%s]' % (newfilename))


def get_pages(filename):
    return PdfFileReader(file(filename, 'rb')).getNumPages()


class Pdf2img:
    def __init__(self, pdf_in):
        self.pdf_in = pdf_in
        self.begin()

    def begin(self):
        get_source = self.pdf_in

        print('source:%s ' % get_source )
        # get_source = sys.argv[1]
        pages = get_pages(get_source)
        # 进程程数
        process_num = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=process_num)
        # 生成一个列表包含所有页码
        # ['test/test1/ab.pdf[0]', 'test/test1/ab.pdf[1]', 'test/test1/ab.pdf[2]', 'test/test1/ab.pdf[3]']
        page_list = [get_source + "[" + str(i) + "]" for i in range(pages)]
        print('=========>>>> Start [Process num: %s]' % (process_num))
        pool.map(process, page_list)
        pool.close()
        pool.join()
        print 'Page Size:%s' % (pages)
        print('<<<========= End')







if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' ,'--input-pdf'      ,dest='pdf_in' ,help="pdf to handle"   ,default='demo.pdf')
    parser.add_argument('-o' ,'--output-dir'     ,dest='dir_out',help="image after handle",default='.\/')
    args = parser.parse_args()
    print("pdf to handle:%s" % args.pdf_in)
    Pdf2img(args.pdf_in)
