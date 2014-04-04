# coding: UTF-8
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
        """
        返回Api字典
        """
        apis = {}

        apis.update(cls.__math_apis())

        return apis

    @classmethod
    def __listarg(cls, func):
        def _(*arg, **kw):
            return func(arg, **kw)

        return _

    @classmethod
    def __math_apis(cls):
        """
        Classmethod
        """
        return {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "arcsin": math.asin,
        "arccos": math.acos,
        "arctan": math.atan,
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,

        "log": cls.__log,
        "log10": math.log10,
        "ln": math.log,

        "pow": pow,
        "exp": math.exp,
        "fact": math.factorial,
        "mod": lambda a, b: a % b,
        "sqrt": math.sqrt,
        "cuberoot": cls.__cuberoot,
        "yroot": cls.__yroot,

        "avg": Supporter.__listarg(cls.__avg),
        "sum": Supporter.__listarg(sum),
        "var": Supporter.__listarg(cls.__var),
        "stdev": Supporter.__listarg(cls.__stdev),
        "varp": Supporter.__listarg(cls.__varp),
        "stdevp": Supporter.__listarg(cls.__stdevp),

        "_e": math.e,
        "_pi": math.pi,

        "num": Decimal,

        "array": cls.__array,
    }

    @staticmethod
    def __log(b, n):
        return math.log(n, b)

    @staticmethod
    def __cuberoot(n):
        return pow(n, 1.0 / 3)

    @staticmethod
    def __yroot(n, y):
        return pow(n, 1.0 / y)

    @staticmethod
    def __avg(l):
        return sum(l) / len(l)

    @staticmethod
    def __var(l):
        n = len(l)
        avg = Supporter.__avg(l)

        if n == 1:return None
        return reduce(lambda s, i:s + (i - avg) ** 2, l, 0.0) / n

    @staticmethod
    def __stdev(l):
        return math.sqrt(Supporter.__var(l))

    @staticmethod
    def __varp(l):
        n = len(l)
        avg = Supporter.__avg(l)
        print avg

        return reduce(lambda s, i:s + (i - avg) ** 2, l, 0.0) / (n - 1)

    @staticmethod
    def __stdevp(l):
        return math.sqrt(Supporter.__varp(l))


    @staticmethod
    def __array(*arg):
        arr = []
        for e in arg:
            if isinstance(e, (list, tuple)):
                arr.extend(Supporter.__array(e))
            else:arr.append(e)
        return tuple(arr)

class Calculator(object):
    """
    计算器
    """
    def __init__(self, ):
        super(Calculator, self).__init__()
        self.__handler = ycpy.YCPY(Supporter.GetApis())

    def format_exp(self, exp):
        fmt_tks = Convertor.format(exp)
        stack = []

        for tk in fmt_tks:
            if tk.type == ElementTypeEnum.NUM or tk.type == ElementTypeEnum.VAR:
                stack.append(str(tk.value))
            elif isinstance(tk.value, operators.UnaryOperator):
                a = stack.pop()
                stack.append(tk.value(a))
            elif isinstance(tk.value, operators.BinaryOperator):
                b = stack.pop()
                a = stack.pop()
                stack.append(tk.value(a,b))

        if len(stack) == 1:
            return stack[-1]

    def save_var(self, var, val):
        if var.startswith("$"):
            var = var.replace("$", "_")
            self.__handler.exec_code("%s=%s" % (var, str(val)))
        else:
            raise ValueError("Var should starts with $")

    def xrun(self, exp):
        res = None
        err = None
        if exp.find(":") != -1:
            i = exp.find(":")
            var = exp[:i]
            exp = exp[i+1:]
            m_var = re.search("(\$\w+)", var)
            if m_var:
                res, err = self.eval(exp)
                self.save_var(m_var.groups()[0], res)
            else:
                raise ValueError("Could not found var name.")
        elif exp.find("=") != -1:
            res, err = self.equation(exp)
        else:
            res, err = self.eval(exp)
        return res, err

    def eval(self, exp, *arg):
        exp = self.format_exp(exp)
        r, o, e = self.__handler.eval_exp(exp)
        self.save_var("$ans", r)
        return r, e

    def equation(self, exp):
        e1, e2 = exp.split("=")
        exp = "(%s)-(%s)" % (e1, e2)
        self.save_var("$$", 1j)
        r, e = self.eval(exp)
        r = -r.real/r.imag
        self.save_var("$$", r)
        return r, e



