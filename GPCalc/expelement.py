# coding: UTF-8
# Name: 表达式元素
# Author: LYC
# Created: 2014-04-03

import re

class ElementType(object):
    """
    表达式元素类型
    """
    def __init__(self, name, pattern):
        super(ElementType, self).__init__()
        self.name = name
        self.regex = re.compile(pattern)

    def __call__(self, obj_str):
        match = self.regex.search(obj_str)
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
    UOP = ElementType("UOP", r"^(\-|\+|[a-z]+\d*)$")#单目运算符
    NUM = ElementType("NUM", r"^(\.|\d)+j?$")#数字
    BOP = ElementType("BOP", r"^(\W+|[a-z]+)$")#二目运算符
    VAR = ElementType("VAR", r"^_[a-z_0-9]+$")#合法变量
    LBK = ElementType("LBK", r"^[\(\[]$")#左括号
    RBK = ElementType("RBK", r"^[\)\]]$")#右括号
    CMM = ElementType("CMM", r"^,$")#逗号
    NON = ElementType("NON", r"^$")#无

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
