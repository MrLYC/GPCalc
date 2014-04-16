# coding: UTF-8
# Name: 表达式元素
# Author: LYC
# Created: 2014-04-03

import re
from gpcalccfg import OPRegex

class ElementType(object):
    """
    表达式元素类型
    """
    def __init__(self, name, regex):
        super(ElementType, self).__init__()
        self.name = name
        self.regex = regex

    def __call__(self, obj_str):
        match = self.regex.search(obj_str)#使用对应的regex来匹配
        if match:return match.group()
        return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class ElementTypeEnum(object):
    """
    表达式元素类型枚举
    """
    UOP = ElementType("UOP", OPRegex.UOPRegex)#单目运算符
    BOP = ElementType("BOP", OPRegex.BOPRegex)#二目运算符
    VAR = ElementType("VAR", OPRegex.VARRegex)#合法变量
    LBK = ElementType("LBK", OPRegex.LBKRegex)#左括号
    RBK = ElementType("RBK", OPRegex.RBKRegex)#右括号
    NUM = ElementType("NUM", OPRegex.NUMRegex)#数字
    NON = ElementType("NON", OPRegex.NONRegex)#无

class Element(object):
    """
    表达式元素
    """
    def __init__(self, value, e_type):
        super(Element, self).__init__()
        self.value = value
        self.type = e_type

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)
