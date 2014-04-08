# coding: UTF-8
# Name: 配置信息
# Author: LYC
# Created: 2014-04-08

import re

class Configuration(object):
    """
    配置
    """
    UserDeclarator = ":"
    VarPrefix = "$"
    FuncPrefix = "#"
    ConstantPrefix = "$$"

    VarRealPrefix = "_"
    FuncRealPrefix = "func_"

    UnknownNumber = "$$"
    AnswerConstant = "$$ans"

    UserVarRegex = re.compile("^\s*(\$[a-z]+\d*)\s*$")
    UserFuncRegex = re.compile("^\s*(#[a-z]+\d*)\s*$")

    HexRegex = re.compile("0x[0-9a-f]+")
    AutoNumFunc = "_"

class OPLEVEL(object):
    """
    运算符优先级与权值
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


class OPRegex(object):
    """
    运算符正则
    """

    UOPRegex = re.compile(r"^(\-|\+|[a-z]\w*)$")
    NUMRegex = re.compile(r"^(\.|\d)+[jl]?$")
    BOPRegex = re.compile(r"^(\W+|[a-z]+)$")
    VARRegex = re.compile(r"^_[a-z_0-9]+$")
    LBKRegex = re.compile(r"^[\(\[]$")
    RBKRegex = re.compile(r"^[\)\]]$")
    CMMRegex = re.compile(r"^,$")
    NONRegex = re.compile(r"^$")