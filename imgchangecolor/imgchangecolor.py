#!/usr/bin/env python2
#
# convertfb - program to adapt image to framebuffer
#
#
# This program is provided under the Gnu General Public License (GPL)
# version 2 ONLY. This program is distributed WITHOUT ANY WARRANTY.
# See the LICENSE file, which should have accompanied this program,
# for the text of the license.
#
# 2016-06-24 by zqb-all <zhuangqiubin@gmail.com>
#
#
# CHANGELOG:
#  2017.06.24 - Version 1.0.0 - The first version

from __future__ import division
VERSION=(1,0,0)
import time
import argparse
from PIL import Image
import progressbar
import math
import sys

def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
                            '=' * int(math.floor(cur * 50 / total)),
                            percent))
    sys.stdout.flush()

class ChangeColor:

    def __init__(self,img_in,img_out,red_s=245,red_e=255,green_s=245,green_e=255,blue_s=245,blue_e=255,red_n=199,green_n=237,blue_n=204):
        self.img_in = img_in
        self.img_out = img_out
        self.red_s = red_s
        self.red_e = red_e
        self.red_n = red_n
        self.green_s = green_s
        self.green_e = green_e
        self.green_n = green_n
        self.blue_s = blue_s
        self.blue_e = blue_e
        self.blue_n = blue_n
        self.begin()

    def begin(self):
        begin_time=time.clock()
        im = Image.open(self.img_in).convert("RGB")
        w, h = im.size
        print("w:%d,h:%d" % (w,h))
        print("r:%d-%d,g:%d-%d,b:%d-%d"
             % (self.red_s,self.red_e,
                self.green_s,self.green_e,
                self.blue_s,self.blue_e))
        for j in range(0,h):
            progressbar(j+1, h)
            for i in range(0,w):
                r,g,b = im.getpixel((i,j))
                if (        r >= self.red_s   and r <= self.red_e
                        and g >= self.green_s and g <= self.green_e
                        and b >= self.blue_s  and b <= self.blue_e):
                        #print ("get pix i:%d,j:%d rgb:%d %d %d"%(i,j,r,g,b) )
                    r = self.red_n
                    g = self.green_n
                    b = self.blue_n
                    im.putpixel((i,j), (r,g,b))
        im.save(self.img_out)
        end_time=time.clock()
        print("done:%d"%(end_time - begin_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' ,'--input'      ,dest='img_in' ,help="image to handle"   ,default='demo.png')
    parser.add_argument('-o' ,'--output'     ,dest='img_out',help="image after handle",default='demo_o.png')
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
    ChangeColor(args.img_in,args.img_out,args.red_s,args.red_e,args.green_s,args.green_e,args.blue_s,args.blue_e,args.red_n,args.green_n,args.blue_n)
