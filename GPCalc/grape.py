﻿# coding: UTF-8
# Name: 默认数值类型
# Author: LYC
# Created: 2014-04-06

import decimal
import re

def grape_operator(func):
    """自动转换"""
    def _(self, o2, *arg, **kw):
        o_type = type(o2)

        if o_type == GrapeArray:raise Exception("unsupport operand type.")

        #decimal不支持与float和complex运算
        if o_type in (float, complex):
            o1 = o_type(self)#转换当前对象为对方类型对象o1
            f = getattr(o1, func.__name__)#获取o1与当前对象同名方法
            res = f(o2)

        else:res = func(self, o2, *arg, **kw)

        #转换成Grape
        if isinstance(res, (float, decimal.Decimal, int)):
            res = Grape(res)

        return res
    return _

def graperesult(method):
    """将结果包装成Grape类型"""
    def _(self, *arg, **kw):
        return Grape(method(self, *arg, **kw))
    return _

def autonum(num):
    """智能数字工厂"""
    if isinstance(num, (Grape, complex)):#复数和Grape直接返回
        return num
    if isinstance(num, tuple):#数组则对每个元素进行转换
        return GrapeArray(autonum(n) for n in num)

    n_str = str(num)
    if n_str.endswith("j"):
        return complex(n_str)
    if n_str.endswith("l"):
        n_str = n_str[:-1]
    if n_str.find(".") == -1:
        n_str += ".0"
    return Grape(n_str)

class GrapeType(type):
    """Grape类的元类"""
    def __init__(cls, name, bases, dct):
        super(GrapeType, cls).__init__(name, bases, dct)

        graperes_lst = (
            "__pos__",
            "__neg__",
            "__abs__",
        )

        grapeop_lst = (
            "__lt__",
            "__gt__",
            "__le__",
            "__ge__",
            "__eq__",
            "__ne__",
            "__add__",
            "__sub__",
            "__mul__",
            "__div__",
            "__mod__",
            "__pow__",
            "__truediv__",
            "__floordiv__",
            "__divmod__",

            "__radd__",
            "__rsub__",
            "__rmul__",
            "__rdiv__",
            "__rmod__",
            "__rpow__",
            "__rtruediv__",
            "__rfloordiv__",
            "__rdivmod__",
        )

        for n in graperes_lst:
            method = getattr(cls, n)
            setattr(cls, n, graperesult(method))

        for n in grapeop_lst:
            method = getattr(cls, n)
            setattr(cls, n, grape_operator(method))

class Grape(decimal.Decimal):
    """
    自动转换的高精度数值
    """
    _grape_str_regex = re.compile(r"(^0+)|(0+$)")
    __metaclass__ = GrapeType

    def __init__(self, data):
        if data == "inf":data = "Infinity"
        elif data == "-inf":data = "-Infinity"

    def __str__(self):
        s = super(Grape, self).__str__()

        dot_idx = s.find(".")
        if dot_idx != -1:
            s = self._grape_str_regex.sub("", s)

        if s.endswith("."):
            s = s[:-1]

        return s

    def __repr__(self):
        return "Grape('%s')" % str(self)


class GrapeArray(tuple):
    """
    数组
    """
    def __str__(self):
        return "[%s]" % ", ".join(map(str, self))