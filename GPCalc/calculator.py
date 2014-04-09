﻿# coding: UTF-8
# Name: 计算器
# Author: LYC
# Created: 2014-04-03

from convertor import Convertor
from expelement import ElementTypeEnum
import operators
import ycpy
import re
from supportor import *
from gpcalccfg import Configuration
from collections import deque

class Calculator(object):
    """
    计算器
    """
    def __init__(self, ):
        super(Calculator, self).__init__()
        self._handler = ycpy.YCPY(Supporter.GetApis())#初始化YCPY

    def format_exp(self, exp):
        """格式化表达式"""
        fmt_tks = Convertor.format(exp)#获得等价的后缀表达式
        stack = []

        #后缀表达式转换
        #参考:http://zh.wikipedia.org/wiki/%E9%80%86%E6%B3%A2%E5%85%B0%E8%A1%A8%E7%A4%BA%E6%B3%95
        for tk in fmt_tks:
            if tk.type == ElementTypeEnum.NUM or tk.type == ElementTypeEnum.VAR:
                #数字和变量直接入栈
                stack.append(str(tk.value))
            elif isinstance(tk.value, operators.Operator):
                #运算符则出栈opnum(可操作数目)个操作数进行转换
                n = tk.value.opnum

                if len(stack) < n:raise Exception("not enough operand")

                args = (stack.pop(i-n) for i in xrange(n)) if n else tuple()
                stack.append(tk.value(*tuple(args)))#指定操作符转换处理

        l = len(stack)
        if l < 1:raise Exception("this is a bug, send it to saber000@vip.qq.com please.")
        elif l == 1:return stack[-1]
        else:raise Exception("unnecessary operand found")

    def save_var(self, vars, vals):
        """保存变量"""
        vars = ",".join(Convertor.format_usrname(v) for v in vars)
        vals = ",".join(str(v) for v in vals)

        self._handler.exec_code("%s = %s" % (vars, vals))

    def del_var(self, vars):
        """删除变量"""
        vars = ",".join(Convertor.format_usrname(v) for v in vars)
        self._handler.exec_code("del %s" % vars)

    def save_func(self, func, exp):
        """保存函数"""
        if func.startswith(Configuration.FuncPrefix):

            if exp.find(Configuration.UserDeclarator) != -1:
                raise Exception("invalid syntax")
            if exp.find("=") != -1:
                raise Exception("invalid syntax")

            #实际成为了YCPY虚拟环境中全局变量
            func = Convertor.format_usrname(func)
            lmd = Supporter.args2list(func_lambda(exp, self))#包装自定义函数
            self._handler.add_api(func, lmd)#加入到虚拟空间中
        else:
            raise Exception("Function should starts with #")

    def xrun(self, exp):
        """智能选择运行的模式"""
        res = None
        err = ""
        out = ""

        if exp.find(Configuration.UserDeclarator) != -1:
            if exp.startswith(Configuration.FuncPrefix):#函数声明
                res, out, err = self.def_func(exp)
            elif exp.startswith(Configuration.VarPrefix):#变量声明
                res, out, err = self.def_var(exp)
            else:raise Exception("unknown operator")

        elif exp.find("=") != -1:#求解方程
            res, out, err = self.equation(exp)

        else:#普通表达式
            res, out, err = self.eval(exp)

        if res == None:res = tuple()
        return res, out, err

    def eval(self, exp, is_pytype = False):
        """计算表达式"""
        if not is_pytype:exp = self.format_exp(exp)#转换成等价的Python表达式

        r, o, e = self._handler.eval_exp(exp)

        if isinstance(r, tuple):
            r = Supporter.tuple(r)

        self.save_var((Configuration.AnswerConstant,), (r,))#保存结果
        return r, o, e

    def equation(self, exp):
        """计算方程"""

        if exp.find(Configuration.ConstantPrefix) == -1:raise Exception("could not found the unknown number")

        #利用Python的暗黑魔法来求解
        #出自:http://code.activestate.com/recipes/365013-linear-equations-solver-in-3-lines/
        #缺点是只能求解一元一次方程
        #未知数不能位于函数参数处和数组里
        #未知数位于分母的方程是分式方程,不属于一元一次方程
        #原理简述:利用复数的虚部系数保存了未知数的系数,其他常数参与计算后成为实部
        #将最后结果的复数实部除以虚部并取反就是未知数的值
        e1, e2 = exp.split("=")
        exp = "(%s)-(%s)" % (e1, e2)
        self.save_var((Configuration.UnknownNumber,), (1j,))#使用复数1j替换未知数
        r, o, e = self.eval(exp)

        if r.imag == 0:raise Exception("could not solve this equation")

        r = -r.real/r.imag#实部除以虚部并取反

        #保存结果
        self.save_var((Configuration.AnswerConstant,), (r,))
        #保存未知数
        self.save_var((Configuration.UnknownNumber,), (r,))
        return r, o, e

    def def_var(self, exp):
        """定义变量"""
        i = exp.find(":")
        var = exp[:i]#预计的变量名
        exp = exp[i+1:]#变量的表达式
        m_var = Configuration.UserVarRegex.search(var)

        if m_var:#确保是正确的命名以防被注入
            res, out, err = self.eval(exp)
            self.save_var((m_var.groups()[0],), (res,))
            return res, out, err
        raise Exception("illegal var name of %s" % var)

    def def_func(self, exp):
        """定义函数"""
        i = exp.find(":")
        name = exp[:i]#预计的函数名
        exp = exp[i+1:]#函数内容

        m_name = Configuration.UserFuncRegex.search(name)

        if m_name:#确保是正确的命名以防被注入
            self.save_func(m_name.groups()[0], exp)

            return None, "", ""
        raise Exception("illegal lambda name of %s" % name)


