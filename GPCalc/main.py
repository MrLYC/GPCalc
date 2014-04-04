# coding: UTF-8
# Name: 主模块
# Author: LYC
# Created: 2014-04-03

import sys
from calculator import Calculator

def by_input():
    calc = Calculator()
    while True:
        exp = raw_input("> ")
        if not exp:break
        err = None
        try:
            r, err = calc.xrun(exp)
            if r != None:print "$ans:", r
        except:
            info = sys.exc_info()
            err = "\n".join([str(i) for i in info]) + "\n"
        if err:
            e = err.split("\n")
            print "===== err ====="
            print e[1]
            print ""

def quick_calc(exps):
    calc = Calculator()
    for exp in exps:
        try:
            r, err = calc.xrun(exp)
            if r != None:print "$ans:", r
        except:
            info = sys.exc_info()
            err = "\n".join([str(i) for i in info]) + "\n"
        if err:
            e = err.split("\n")
            print "===== err ====="
            print e[1]
            print ""

def main(argv):
    if len(argv) == 1:
        by_input()
    else:
        quick_calc(argv[1:])

if __name__ == '__main__':
    main(sys.argv)

