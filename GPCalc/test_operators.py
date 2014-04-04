# coding: UTF-8
# Name: operators单元测试
# Author: LYC
# Created: 2014-04-03

import sys
import pytest

from operators import *

#Operator类
#-------------------------------------------------------------------------------
def test_Operator():
    a = Operator("+", 0, 1)
    b = Operator("-", 1, 1)
    c = Operator("*", 1, 2)
    d = Operator("*", 1, 2)

    assert (a<b) == True
    assert (c>a) == True
    assert (a<=b) == True
    assert (c<=b) == True
    assert (b>=a) == True
    assert (b>=c) == True
    assert (d==c) == True
    assert (d!=c) == False

    assert str(a) == "+"
#-------------------------------------------------------------------------------

#UnaryOperator类
#-------------------------------------------------------------------------------
def test_UnaryOperator():
    a = UnaryOperator("+")

    assert a.level == OPLEVEL.UOP
    assert a.opnum == 1
    assert str(a) == "+"
    assert eval(a(5)) == 5.0
    assert eval(a("5")) == 5.0
#-------------------------------------------------------------------------------

#operator_factory函数与BinaryOperator类
#-------------------------------------------------------------------------------
def test_operator_factory():
    a = operator_factory("+", True)
    b = operator_factory("+")
    c = operator_factory("sum")

    assert isinstance(a, UnaryOperator)
    assert isinstance(b, BinaryOperator)
    assert isinstance(c, UnaryOperator)
    assert a > b
    assert b.opnum == 2
    assert str(a) == "+"

    a = operator_factory("pow", True)
    b = operator_factory("sin")
    c = operator_factory("*")
    d = operator_factory("/")
    e = operator_factory("mod")
    f = operator_factory("^")
    g = operator_factory("+")

    assert isinstance(a, UnaryOperator)
    assert isinstance(b, UnaryOperator)
    assert isinstance(c, BinaryOperator)
    assert isinstance(d, BinaryOperator)
    assert isinstance(e, BinaryOperator)
    assert isinstance(f, BinaryOperator)
    assert isinstance(g, BinaryOperator)

    assert a >= b >= f >= e > d >= c > g

#-------------------------------------------------------------------------------

def main():
    pytest.main("-x '%s'" % sys.argv[0])

if __name__ == '__main__':
    main()
