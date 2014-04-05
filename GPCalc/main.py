# coding: UTF-8
# Name: 主模块
# Author: LYC
# Created: 2014-04-03

import sys
from calculator import Calculator

def by_input():
    """输入表达式"""
    print """
=================== Info =====================
GPClac v0.1 created by LYC built on 03/04/2014

    Help for GPCalc
GPCalc can evaluate expression strings from
stdin or start up arguments.
Welcome to visit and get the detail documents
on: https://git.oschina.net/Mr_LYC/GPCalc/

    Features
Evaluation:
    fact(100) / 2

Define a var:
    $varname:expression
    You can use your var like $varname in your
    expression later.

Solve an equation:
    1 + 2 * $$ = 3 / 4
    $$ is representing the unknown number.

Hope you to enjoy it!
"""


    calc = Calculator()
    while True:
        exp = raw_input("> ")
        if not exp:break
        #错误信息
        err = None
        try:
            #智能执行并返回结果和错误信息
            r, err = calc.xrun(exp)
            if r != None:print "$ans:", r
        except:
            info = sys.exc_info()
            err = "\n".join([str(i) for i in info]) + "\n"
        if err:
            e = err.split("\n")
            print "==================== error ===================="
            print e[1] #只输出错误信息
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
