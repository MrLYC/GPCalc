# coding: UTF-8
# Name: 默认数值类型
# Author: LYC
# Created: 2014-04-06

import decimal

def grape_operator(func):
    """自动转换"""
    def _(self, o2, *arg, **kw):
        o_type = type(o2)

        if o_type == tuple:raise Exception("unsupport operand type.")

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


def autonum(n_str):
    """数字字符串"""
    n_str = str(n_str)
    if n_str.endswith("j"):
        return complex(n_str)
    if n_str.endswith("l"):
        n_str = n_str[:-1]
    if n_str.find(".") == -1:
        n_str += ".0"
    return Grape(n_str)

class GrapeType(type):
    """grape类的类"""
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
    __metaclass__ = GrapeType
    def __repr__(self):
        return str(self)
