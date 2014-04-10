# coding: UTF-8
# Name: convertor单元测试
# Author: LYC
# Created: 2014-04-03

import sys
import pytest

from convertor import Convertor
from expelement import Element, ElementTypeEnum
import operators

#Convertor类
#-------------------------------------------------------------------------------

def test_preprocessing():
    case = (
        ("1+1", "1+1"),
        ("1 + 1 ", "1 + 1"),
        (" 1 +1", "1 +1"),
        ("1 pOw $e", "1 pow _e"),
    )
    for c, r in case:
        assert Convertor.preprocessing(c) == r

def test_grapetoken():
    exp = "sum([-1+1*2,4+5/2^2,3mod mod(3,2)])"
    res = (
        "sum",
        "(",
        "(",
        "-",
        "1",
        "+",
        "1",
        "*",
        "2",
        ",",
        "4",
        "+",
        "5",
        "/",
        "2",
        "**",
        "2",
        ",",
        "3",
        "%",
        "mod",
        "(",
        "3",
        ",",
        "2",
        ")",
        ")",
        ")",
    )

    rr = Convertor.tokenize(exp)
    for c,r in zip(rr, res):
        assert str(c.value) == r

    assert rr[3].type == ElementTypeEnum.UOP
    assert isinstance(rr[0].value, operators.UnaryOperator)
    assert rr[5].type == ElementTypeEnum.BOP
    assert isinstance(rr[5].value, operators.BinaryOperator)

def test_format():
    case = (
       ("8-(3+2*6)/5+4", "8 3 2 6 * + 5 / - 4 +"),
       ("((5+7)/3*7-(3*2))+(7-3)*3+2*5+4*5+1*6+1*5", "5 7 + 3 / 7 * 3 2 * - 7 3 - 3 * + 2 5 * + 4 5 * + 1 6 * + 1 5 * +"),
       ("1*((2+3) /2) ^5", "1 2 3 + 2 / 5 ** *"),
       ("-1+((2+3)*4/5)", "1 - 2 3 + 4 * 5 / +"),
       ("-1+-5", "1 - 5 - +"),
       ("pow(3,2)+ sin(45)", "3 2 , pow 45 sin +"),
       ("-$a+$b*(-$c+$d)+$e", "_a - _b _c - _d + * + _e +"),
       ("pOw(1*(2+3), 6+5)", "1 2 3 + * 6 5 + , pow"),
       ("-1+5*-6", "1 - 5 6 - * +"),
       ("Sum([1+1,5+6*7,POW (3,2)])", "1 1 + 5 6 7 * + , 3 2 , pow , sum"),
       ("5/ 4mod sin(1)+SUm([1,2])^3.5* 2-4", "5 4 1 sin % / 1 2 , sum 3.5 ** 2 * + 4 -"),
       ("4", "4"),
       ("-sin(45)", "45 sin -"),
       ("-+-+sin(45)", "45 sin + - + -"),
       ("$var", "_var"),
       ("-(+5+6)", "5 + 6 + -"),
       ("$vAr", "_var"),
    )

    for c, r in case:
        rr = Convertor.format(c)
        assert " ".join(map(str, rr)) == r
#-------------------------------------------------------------------------------


def main():
    pytest.main("-x '%s'" % sys.argv[0])

if __name__ == '__main__':
    main()
