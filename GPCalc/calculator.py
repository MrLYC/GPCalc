﻿# coding: UTF-8
# Name: 计算器
# Author: LYC
# Created: 2014-04-03

from convertor import Convertor
from expelement import ElementTypeEnum
import operators
import ycpy
import math
from decimal import Decimal
import re

class Supporter(object):
    """
    Calcultor Supporter
    """

    @classmethod
    def GetApis(cls):
        """返回Api字典"""
        apis = {}

        apis.update(cls.__math_apis())
        apis.update(cls.__const_apis())
        apis.update(cls.__tools_apis())

        #此字典的键为YCPY中的引用名称
        #是虚拟空间中名称和外部空间对象的映射
        return apis

    @classmethod
    def __args2list(cls, func):
        """将多参数或嵌套数组打包和降维成一维数组的装饰器"""
        def _(*arg, **kw):
            return func(Supporter.tuple(arg), **kw)

        return _

    @classmethod
    def __list2args(cls, func):
        """将数组展开成多个参数列表的装饰器"""
        def _(*arg, **kw):
            return func(*Supporter.tuple(arg), **kw)

        return _

    @classmethod
    def __math_apis(cls):
        """数学函数"""
        return {
        "sin": cls.__list2args(math.sin),
        "cos": cls.__list2args(math.cos),
        "tan": cls.__list2args(math.tan),
        "arcsin": cls.__list2args(math.asin),
        "arccos": cls.__list2args(math.acos),
        "arctan": cls.__list2args(math.atan),
        "sinh": cls.__list2args(math.sinh),
        "cosh": cls.__list2args(math.cosh),
        "tanh": cls.__list2args(math.tanh),

        "log": cls.__list2args(cls.__log),
        "log10": cls.__list2args(math.log10),
        "ln": cls.__list2args(lambda a: math.log(a)),

        "pow": cls.__list2args(pow),
        "exp": cls.__list2args(math.exp),
        "fact": cls.__list2args(math.factorial),
        "mod": cls.__list2args(lambda a, b: a % b),
        "sqrt": cls.__list2args(math.sqrt),
        "cuberoot": cls.__list2args(cls.__cuberoot),
        "yroot": cls.__list2args(cls.__yroot),

        "avg": cls.__args2list(cls.__avg),
        "sum": cls.__args2list(sum),
        "var": cls.__args2list(cls.__var),
        "stdev": cls.__args2list(cls.__stdev),
        "varp": cls.__args2list(cls.__varp),
        "stdevp": cls.__args2list(cls.__stdevp),
        }


    @classmethod
    def __const_apis(cls):
        """常量对象"""
        return {
        "_e": math.e,
        "_pi": math.pi,
        }


    @classmethod
    def __tools_apis(cls):
        """扩展函数"""
        return {
        "tuple": cls.tuple,
        "val": cls.__args2list(cls.__val),
        "cell": cls.__args2list(cls.__int),
        }

    @staticmethod
    def __log(b, n):
        """以 nBase 为底的，值 x 的对数"""
        return math.log(n, b)

    @staticmethod
    def __cuberoot(n):
        """开三次方根"""
        return pow(n, 1.0 / 3)

    @staticmethod
    def __yroot(n, y):
        """求值 x 的 y 次方根"""
        return pow(n, 1.0 / y)

    @staticmethod
    def __avg(l):
        """集合的算术平均值"""
        return sum(l) / len(l)

    @staticmethod
    def __var(l):
        """集合的估算方差"""
        n = len(l)
        avg = Supporter.__avg(l)

        if n == 1:return 0.0
        return reduce(lambda s, i:s + (i - avg) ** 2, l, 0.0) / n

    @staticmethod
    def __stdev(l):
        """集合的估算标准差"""
        return math.sqrt(Supporter.__var(l))

    @staticmethod
    def __varp(l):
        """集合的总体方差"""
        n = len(l)
        avg = Supporter.__avg(l)

        if n == 1:return 0.0
        return reduce(lambda s, i:s + (i - avg) ** 2, l, 0.0) / (n - 1)

    @staticmethod
    def __stdevp(l):
        """集合的总体标准偏差"""
        return math.sqrt(Supporter.__varp(l))

    @staticmethod
    def __val(n):
        """各种进制下的整型表示方式"""
        n = map(int, n)
        print "Dec: (%s)" % ",".join(map(str, n))
        print "Hex: (%s)" % ",".join(map(lambda n: str(hex(n)), n))
        print "Oct: (%s)" % ",".join(map(lambda n: str(oct(n)), n))
        print "Bin: (%s)" % ",".join(map(lambda n: str(bin(n)), n))
        return Supporter.__int(n)

    @staticmethod
    def __int(n):
        """取整"""
        return tuple(map(lambda i:float(int(i)), n))

    @staticmethod
    def tuple(arg):
        """参数包装成数组(tuple)"""
        arr = []
        if isinstance(arg, tuple):
            for e in arg:
                if isinstance(e, (list, tuple)):
                    arr.extend(Supporter.tuple(e))
                else:arr.append(e)
        else:arr.append(arg)
        return tuple(arr)



class Calculator(object):
    """
    计算器
    """
    def __init__(self, ):
        super(Calculator, self).__init__()
        self.__handler = ycpy.YCPY(Supporter.GetApis())#初始化YCPY

    def format_exp(self, exp):
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

                args = (stack.pop(i-n) for i in xrange(n)) if n else []
                stack.append(tk.value(*tuple(args)))

        l = len(stack)
        if l < 1:raise Exception("this is a bug, send it to saber000@vip.qq.com please.")
        elif l == 1:return stack[-1]
        else:raise Exception("unnecessary operand found")

    def save_var(self, var, val):
        if var.startswith("$"):
            #变量实际成为了YCPY虚拟环境中_开头的全局变量
            var = var.replace("$", "_")
            #利用YCPY能够执行代码块的功能保存
            self.__handler.exec_code("%s=%s" % (var, str(val)))
        else:
            raise Exception("Var should starts with $")

    def xrun(self, exp):
        res = None
        err = ""
        out = ""
        if exp.find(":") != -1:#变量声明
            i = exp.find(":")
            var = exp[:i]#预计的变量名
            exp = exp[i+1:]#变量的表达式
            m_var = re.search("^\s*(\$[a-z_]+\d*)\s*$", var)

            if m_var:#确保是正确的命名以防被注入
                res, out, err = self.eval(exp)
                self.save_var(m_var.groups()[0], res)
            else:raise Exception("illegal var name of %s" % var)

        elif exp.find("=") != -1:#求解方程
            res, out, err = self.equation(exp)

        else:#普通表达式
            res, out, err = self.eval(exp)

        return res, out, err

    def eval(self, exp, *arg):
        exp = self.format_exp(exp)#转换成等价的Python表达式
        r, o, e = self.__handler.eval_exp(exp)

        if isinstance(r, tuple):
            r = Supporter.tuple(r)

        self.save_var("$ans", r)#保存结果
        return r, o, e

    def equation(self, exp):
        #利用Python的暗黑魔法来求解
        #出自:http://code.activestate.com/recipes/365013-linear-equations-solver-in-3-lines/
        #缺点是只能求解一元一次方程
        #未知数不能位于函数参数处和数组里
        #未知数位于分母的方程是分式方程,不属于一元一次方程
        #原理简述:利用复数的虚部系数保存了未知数的系数,其他常数参与计算后成为实部
        #将最后结果的复数实部除以虚部并取反就是未知数的值
        e1, e2 = exp.split("=")
        exp = "(%s)-(%s)" % (e1, e2)
        self.save_var("$$", 1j)#使用复数1j替换未知数
        r, o, e = self.eval(exp)
        r = -r.real/r.imag#实部除以虚部并取反

        #保存结果
        self.save_var("$ans", r)
        #保存未知数
        self.save_var("$$", r)
        return r, o, e

