# coding: UTF-8
# Name:
# Author: LYC
# Created: 2014-04-03

import re

class OPLEVEL(object):
    """
    优先级
    """
    LBK = 00,
    CMM = 10,
    ADD = 20,
    SUB = 20,
    MUL = 30,
    DIV = 30,
    MOD = 40,
    POW = 40,
    UOP = 50,

class Operator(object):
    """
    运算符
    """
    def __init__(self, original, level = 0, opnum = 0):
        super(Operator, self).__init__()
        self.original = original
        self.level = level #权值
        self.opnum = opnum #可操作数

    def __call__(self, *arg):
        return str(arg)

    def __str__(self):
        return self.original

    def __repr__(self):
        return str(self.original)

    def __lt__(self, op):
        return self.level < op.level

    def __gt__(self, op):
        return self.level > op.level

    def __le__(self, op):
        return self.level <= op.level

    def __ge__(self, op):
        return self.level >= op.level

    def __eq__(self, op):
        if isinstance(op, str):return self.original == op
        if self.original != op.original:return False
        if self.level != op.level:return False
        if self.opnum != op.opnum:return False
        return True

    def __ne__(self, op):
        return not self == op

class UnaryOperator(Operator):
    """
    单目运算符
    """
    def __init__(self, original):
        super(UnaryOperator, self).__init__(original, OPLEVEL.UOP, 1)

    def __call__(self, operand):
        return "(%s(%s))" % (self.original, str(operand))


class BinaryOperator(Operator):
    """
    双目运算符
    """
    def __init__(self, original, level):
        super(BinaryOperator, self).__init__(original, level, 2)

    def __call__(self, operand1, operand2):
        return "((%s) %s (%s))" % (str(operand1), self.original, str(operand2))

class ListOperator(BinaryOperator):
    """
    列表运算符
    """
    def __call__(self, operand1, operand2):
        return "%s, %s" % (str(operand1), str(operand2))

def operator_factory(original, unary = False):
    """
    运算符工厂
    original: 运算符表示
    unary: 限定为单目,请用于单目的+-
    """

    if unary:return UnaryOperator(original)
    if original == "+":return BinaryOperator(original, OPLEVEL.ADD)
    if original == "-":return BinaryOperator(original, OPLEVEL.SUB)
    if original == "*":return BinaryOperator(original, OPLEVEL.MUL)
    if original == "/":return BinaryOperator(original, OPLEVEL.DIV)
    if original == ",":return ListOperator(original, OPLEVEL.CMM)
    if original == "%":return BinaryOperator(original, OPLEVEL.MOD)
    if original == "**":return BinaryOperator(original, OPLEVEL.POW)
    if original == "mod":return BinaryOperator("%", OPLEVEL.MOD)
    if original == "^":return BinaryOperator("**", OPLEVEL.POW)
    if original == "(":return Operator(original, OPLEVEL.LBK)
    if original == ")":return Operator(original)
    return UnaryOperator(original)
