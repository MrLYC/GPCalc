# coding: UTF-8
# Name: 默认数值类型
# Author: LYC
# Created: 2014-04-06

import decimal

class Gray(decimal.Decimal):
    """
    高精度数值
    """

    def __repr__(self):
        return str(self)

    @staticmethod
    def gray_operator(func):
        """自动转换"""
        def _(self, o2, *arg, **kw):
            o_type = type(o2)

            #decimal不支持与float和complex运算
            if o_type in (float, complex):
                o1 = o_type(self)#转换当前对象为对方类型对象o1
                f = getattr(o1, func.__name__)#获取o1与当前对象同名方法
                res = f(o2)

            else:res = func(self, o2, *arg, **kw)

            #转换成Gray
            if isinstance(res, (float, decimal.Decimal, int)):
                res = Gray(res)

            return res
        return _

    @staticmethod
    def grayresult(method):
        """将结果包装成Gray类型"""
        def _(self, *arg, **kw):
            return Gray(method(self, *arg, **kw))
        return _


Gray.__pos__ = Gray.grayresult(Gray.__pos__)
Gray.__neg__ = Gray.grayresult(Gray.__neg__)
Gray.__abs__ = Gray.grayresult(Gray.__abs__)


Gray.__lt__ = Gray.gray_operator(Gray.__lt__)
Gray.__gt__ = Gray.gray_operator(Gray.__gt__)
Gray.__le__ = Gray.gray_operator(Gray.__le__)
Gray.__ge__ = Gray.gray_operator(Gray.__ge__)
Gray.__eq__ = Gray.gray_operator(Gray.__eq__)
Gray.__ne__ = Gray.gray_operator(Gray.__ne__)

Gray.__add__ = Gray.gray_operator(Gray.__add__)
Gray.__sub__ = Gray.gray_operator(Gray.__sub__)
Gray.__mul__ = Gray.gray_operator(Gray.__mul__)
Gray.__div__ = Gray.gray_operator(Gray.__div__)
Gray.__mod__ = Gray.gray_operator(Gray.__mod__)
Gray.__pow__ = Gray.gray_operator(Gray.__pow__)
Gray.__truediv__ = Gray.gray_operator(Gray.__truediv__)
Gray.__floordiv__ = Gray.gray_operator(Gray.__floordiv__)
Gray.__divmod__ = Gray.gray_operator(Gray.__divmod__)

Gray.__radd__ = Gray.gray_operator(Gray.__radd__)
Gray.__rsub__ = Gray.gray_operator(Gray.__rsub__)
Gray.__rmul__ = Gray.gray_operator(Gray.__rmul__)
Gray.__rdiv__ = Gray.gray_operator(Gray.__rdiv__)
Gray.__rmod__ = Gray.gray_operator(Gray.__rmod__)
Gray.__rpow__ = Gray.gray_operator(Gray.__rpow__)
Gray.__rtruediv__ = Gray.gray_operator(Gray.__rtruediv__)
Gray.__rfloordiv__ = Gray.gray_operator(Gray.__rfloordiv__)
Gray.__rdivmod__ = Gray.gray_operator(Gray.__rdivmod__)