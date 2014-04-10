# coding: UTF-8
# Name: 计算器的支持
# Author: LYC
# Created: 2014-04-06

import math
import cmath
import re
from gpcalccfg import Configuration
from collections import deque

class func_lambda(object):
    """函数类"""
    def __init__(self, exp, hdlr):
        self._handler = hdlr #所属计算器
        self.exp = hdlr.format_exp(exp) #先转换对应的表达式

    def __call__(self, arg_lst = tuple()):
        var_lst = ["%s0" % Configuration.VarPrefix]
        var_lst.extend(["%s%d"%(Configuration.VarPrefix,(i+1)) for i in xrange(len(arg_lst))])

        val_lst = [arg_lst]
        val_lst.extend(arg_lst)

        self._handler.save_var(var_lst, val_lst)#保存参数

        r, o, e = self._handler.eval(self.exp, True)

        self._handler.del_var(var_lst) #清除变量

        if o:
            print o

        if e:
            e = e.split("\n")
            raise Exception(e[1])
        return r

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
    def args2list(cls, func):
        """将多参数或嵌套数组打包和降维成一维数组的装饰器"""
        def _(*arg, **kw):
            return func(Supporter.tuple(arg), **kw)

        return _

    @classmethod
    def list2args(cls, func):
        """将数组展开成多个参数列表的装饰器"""
        def _(*arg, **kw):
            return func(*Supporter.tuple(arg), **kw)

        return _

    @classmethod
    def __math_apis(cls):
        """数学函数"""
        return {
        "sin": cls.list2args(lambda a:math.sin(math.radians(a))),
        "cos": cls.list2args(lambda a:math.cos(math.radians(a))),
        "tan": cls.list2args(lambda a:math.tan(math.radians(a))),
        "arcsin": cls.list2args(lambda r:math.degrees(math.asin(r))),
        "arccos": cls.list2args(lambda r:math.degrees(math.acos(r))),
        "arctan": cls.list2args(lambda r:math.degrees(math.atan(r))),

        "rsin": cls.list2args(math.sin),
        "rcos": cls.list2args(math.cos),
        "rtan": cls.list2args(math.tan),
        "rarcsin": cls.list2args(math.asin),
        "rarccos": cls.list2args(math.acos),
        "rarctan": cls.list2args(math.atan),

        "sinh": cls.list2args(math.sinh),
        "cosh": cls.list2args(math.cosh),
        "tanh": cls.list2args(math.tanh),

        "log": cls.list2args(math.log),
        "log10": cls.list2args(math.log10),
        "ln": cls.list2args(lambda a: math.log(a)),

        "pow": cls.list2args(pow),
        "exp": cls.list2args(math.exp),
        "fact": cls.list2args(math.factorial),
        "mod": cls.list2args(lambda a, b: a % b),
        "sqrt": cls.list2args(math.sqrt),
        "cuberoot": cls.list2args(cls.__cuberoot),
        "yroot": cls.list2args(cls.__yroot),

        "avg": cls.args2list(cls.__avg),
        "sum": cls.args2list(sum),
        "var": cls.args2list(cls.__var),
        "stdev": cls.args2list(cls.__stdev),
        "varp": cls.args2list(cls.__varp),
        "stdevp": cls.args2list(cls.__stdevp),

        "floor": cls.args2list(cls.__floor),
        "len": cls.args2list(len),

        "rad": cls.list2args(math.radians),
        "ang": cls.list2args(math.degrees),

        "zsqrt": cls.list2args(cmath.sqrt),
        "zexp": cls.list2args(cmath.exp),

        "zlog": cls.list2args(cmath.log),
        "zlog10": cls.list2args(cmath.log10),
        "zln": cls.list2args(lambda a: cmath.log(a)),

        "zsin": cls.list2args(cmath.sin),
        "zcos": cls.list2args(cmath.cos),
        "ztan": cls.list2args(cmath.tan),
        "zarcsin": cls.list2args(cmath.asin),
        "zarccos": cls.list2args(cmath.acos),
        "zarctan": cls.list2args(cmath.atan),
        "zsinh": cls.list2args(cmath.sinh),
        "zcosh": cls.list2args(cmath.cosh),
        "ztanh": cls.list2args(cmath.tanh),

        "real": cls.list2args(lambda n: n.real if isinstance(n, complex) else n),
        "imag": cls.list2args(lambda n: n.imag if isinstance(n, complex) else 0),
        }

    @classmethod
    def __const_apis(cls):
        """常量对象"""
        return {
        "__0": tuple(),#空
        "__ans": 1871084291.0,#我的电话

        "__e": math.e,#自然底数
        "__pi": math.pi,#圆周率
        "__c": 299792458,#真空中光速
        "__h": 6.62606896*math.pow(10,-34),#普朗克常数
        "__g": 6.67428*math.pow(10,-11), #引力常数
        "__f": 96485.309,#法拉第常数
        }

    @classmethod
    def __tools_apis(cls):
        """扩展函数"""
        return {
        "tuple": cls.tuple,
        "val": cls.args2list(cls.__val),
        "head": cls.args2list(lambda l: l[0] if l else tuple()),
        "tail": cls.args2list(lambda l: l[1:]),
        "left": cls.args2list(lambda l: l[:len(l)/2]),
        "right": cls.args2list(lambda l: l[len(l)/2:]),
        }

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
    def __floor(n):
        """取整"""
        return tuple(map(lambda i:type(i)(re.sub("\.\d*",".0", str(i))), n))

    @staticmethod
    def tuple(arg):
        """参数包装成数组(tuple)"""
        arr = deque()
        if isinstance(arg, tuple):
            for e in arg:
                if isinstance(e, (list, tuple)):
                    arr.extend(Supporter.tuple(e))
                else:arr.append(e)
        else:arr.append(arg)
        return tuple(arr)