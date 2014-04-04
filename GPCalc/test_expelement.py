# coding: UTF-8
# Name: expelement单元测试
# Author: LYC
# Created: 2014-04-03

import sys
import pytest

import expelement

#ElementType类
#-------------------------------------------------------------------------------
def test_ElementType():
    et = expelement.ElementType("abc", "\d*")

    assert str(et) == "abc"
    assert et("132.5") == "132"
    assert et(".5") == ""
    assert et("5sd") == "5"

#-------------------------------------------------------------------------------

#ElementTypeEnum类
#-------------------------------------------------------------------------------
def test_ElementTypeEnum():
    ElementTypeEnum = expelement.ElementTypeEnum
    cases = (
        "1", #0
        "34",
        ".4",
        "4.4",
        "87.",
        "-1", #5
        "-",
        "+",
        "*",
        "/",
        "mod", #10
        "%",
        "**",
        "sin",
        "cos(",
        "log10", #15
        ",",
        "(",
        ")",
        "[",
        "]", #20
        "{",
        "()",
        ",,",
        "((",
        "", #25
        "))",
        "10pi",
        "pi",
        "x",
        "([", #30
        "_e",
        "_r1",
        "__",
    )

    types = {
        ElementTypeEnum.BOP: (6,7,8,9,10,11,12,13,16,17,18,19,20,21,22,23,24,26,28,29,30),
        ElementTypeEnum.CMM: (16,),
        ElementTypeEnum.LBK: (17,19),
        ElementTypeEnum.NON: (25,),
        ElementTypeEnum.NUM: (0,1,2,3,4),
        ElementTypeEnum.RBK: (18,20),
        ElementTypeEnum.UOP: (6,7,10,13,15,28,29),
        ElementTypeEnum.VAR: (31,32,33),
    }

    for tp, true_case in types.items():
        for i, c in enumerate(cases):
            if i in true_case:
                assert tp(c) != None
            else:
                assert tp(c) == None
#-------------------------------------------------------------------------------

def main():
    pytest.main("-x '%s'" % sys.argv[0])

if __name__ == '__main__':
    main()
