# coding: UTF-8
# Name: grapetokenizer单元测试
# Author: LYC
# Created: 2014-03-28

import sys
import pytest
import grapetokenizer

def test_grapetoken():
    case = (
        ("2014-0o3-0x1a", (("NUM", "2014"),("BOP", "-"),("NUM", "3"),("BOP", "-"),("NUM", "26"))),
        ("1991", (("NUM", "1991"),)),

        ("sin(1.952)", (("UOP", "sin"),("LBK", "("),("NUM", "1.952"),("RBK", ")"))),
        ("cos(3.8)", (("UOP", "cos"),("LBK", "("),("NUM", "3.8"),("RBK", ")"))),
        ("-arctan(0.8)", (("UOP", "-"),("UOP", "arctan"),("LBK", "("),("NUM", "0.8"),("RBK", ")"))),
        ("sinh(0.8)-cosh(.4)*tanh(-1.8)", (("UOP", "sinh"),("LBK", "("),("NUM", "0.8"),("RBK", ")"),("BOP", "-"),("UOP", "cosh"),("LBK", "("),("NUM", ".4"),("RBK", ")"),("BOP", "*"), ("UOP", "tanh"),("LBK", "("),("UOP", "-"), ("NUM", "1.8"),("RBK", ")"))),

        ("-  log(2,  8)", (("UOP", "-"),("UOP", "log"),("LBK", "("),("NUM", "2"),("CMM", ","),("NUM", "8"),("RBK", ")"))),
        ("log10(65535000)", (('UOP', 'log10'), ('LBK', '('), ('NUM', '65535000'), ('RBK', ')'))),
        ("sum([84.3,.005])", (("UOP", "sum"),("LBK", "("),("LBK", "["),("NUM", "84.3"),("CMM", ","),("NUM", ".005"),("RBK", "]"),("RBK", ")"))),
        ("1*(4+5)", (("NUM", "1"),("BOP", "*"),("LBK", "("),("NUM", "4"),("BOP", "+"),("NUM", "5"),("RBK", ")"))),
    )

    for c, r in case:
        gt = grapetokenizer.GrapeToken(c)
        res = gt()

        t = res[-1]
        assert str(t.type) == "NON"
        assert str(t.value) == ""

        for r1, r2 in zip(r, res[:-1]):
            assert r1[0] == str(r2.type)
            assert r1[1] == str(r2.value)


def main():
    pytest.main("-x '%s'" % sys.argv[0])

if __name__ == '__main__':
    main()
