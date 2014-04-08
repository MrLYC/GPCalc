# coding: UTF-8
# Name: 默认数值类型
# Author: LYC
# Created: 2014-04-06

import decimal

def gray_operator(func):
    """自动转换"""
    def _(self, o2, *arg, **kw):
        o_type = type(o2)

        if o_type == tuple:raise Exception("unsupport operand type.")

        #decimal不支持与float和complex运算
        if o_type in (float, complex):
            o1 = self
            if o_type == tuple:o1 = tuple([self])
            else:o1 = o_type(self)#转换当前对象为对方类型对象o1
            f = getattr(o1, func.__name__)#获取o1与当前对象同名方法
            res = f(o2)

        else:res = func(self, o2, *arg, **kw)

        #转换成Gray
        if isinstance(res, (float, decimal.Decimal, int)):
            res = Gray(res)

        return res
    return _

def grayresult(method):
    """将结果包装成Gray类型"""
    def _(self, *arg, **kw):
        return Gray(method(self, *arg, **kw))
    return _

class GrayType(type):
    """Gray类的类"""
    def __init__(cls, name, bases, dct):
        super(GrayType, cls).__init__(name, bases, dct)

        grayres_lst = (
            "__pos__",
            "__neg__",
            "__abs__",
        )

        grayop_lst = (
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

        for n in grayres_lst:
            method = getattr(cls, n)
            setattr(cls, n, grayresult(method))

        for n in grayop_lst:
            method = getattr(cls, n)
            setattr(cls, n, gray_operator(method))

class Gray(decimal.Decimal):
    """
    自动转换的高精度数值
    """
    __metaclass__ = GrayType
    def __repr__(self):
        return str(self)
