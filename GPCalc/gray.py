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
        """Static method"""
        def _(self, o2, *arg, **kw):
            o_type = type(o2)

            if o_type in (float, complex):
                o1 = o_type(self)
                f = getattr(o1, func.__name__)
                return f(o2)

            res = func(self, o2, *arg, **kw)
            if isinstance(res, decimal.Decimal):
                return Gray(res)
            return res
        return _

    @staticmethod
    def grayresult(method):
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