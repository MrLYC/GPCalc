# coding: UTF-8
# Name: 单元测试
# Author: LYC
# Created: 2014-04-03

import sys
import pytest
import calculator

@pytest.fixture
def Calculator_Eval():
    calc = calculator.Calculator()
    def _(exp):
        r, e = calc.eval(exp)
        return r
    return _

@pytest.fixture
def Calculator_Xrun():
    calc = calculator.Calculator()
    def _(exp):
        r, e = calc.xrun(exp)
        return r
    return _


def is_equal(a, b, *arg):
    return abs(a - b) < 0.1 ** 10

def test_simple_exp(Calculator_Eval):
    test = (
        ("2014-03-26", 1985),
        ("1991", 1991),

        ("sin(1.952)", 0.9282174959159),
        ("cos(3.8)", -0.7909677119144),
        ("tan(2.6)", -0.6015966130898),
        ("arcsin(0.84)", 0.9972832223718),
        ("arcCos(-0.8)", 2.4980915447965),
        ("-arcTan(0.8)", -0.6747409422236),

        ("sinh(0.8)-cosh(.4)*tanh(-1.8)", 1.9116718041662),

        ("-  log(2,  8)", -3),
        ("  ln(4)", 1.3862943611199),
        (" log10     (65535000)", 7.8164733037652),

        ("pow(11, 10)", 25937424601),
        ("fact(100)", 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000),
        ("sqrt(122.5)", 11.0679718105893),
        ("cuberoot(1122.5)", 10.3927093873672),
        ("yroot(65539, 12.5)", 2.4283986616318),

        ("sum([84.3,.005,36,12,1.3,6.2])", 139.805),
        ("avg([5.56,1,541,3,411,.9,sin(45)])", 137.6158433606477),
        ("var([12.5, 13, 18, 11.8, 2.3, 7])", 24.5422222222222),
        ("varp([9.0, 1.0, 1.0, 1.0, 0.0, 0.0, 4.0, 16.0])", 32.5714285714286),
        ("stdev([0.2, 0.7, .4,-.3,-.7])", 0.5003998401279),
        ("stdevp([999,888.7,777.2,-666.4,2])", 713.3585073439582),

        ("5*6+81/23mod 74*2^8", 931.5652173913044),
        ("2 * 3^2 + 2 / 3mod 2 - 1", 19),
        ("-.12345+54321*123/321^2mod(sum([-1+10^2*sin(cos(tan(100))),arcsin(-1+1-1),log(100,10)*log10(1000)/ln(exp(1)),cuberoot(sqrt(fact(10)*mod(5,3)))*yroot(5,2),avg([3,4,5,6]),sum([987,253])*var([1,11,111,1111])/stdev([123,321,456,654,789,987])]))", 64.71950571665647),
        ("5mod(mod(2,3mod(2.1)))", 0.2),
        ("fact(100)", 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000),
        ("sum((([1,2,3,4,5,6,7]))) ", 28),
        ("1---5", -4),
        ("-sin(-+2)", 0.90929742682568),
    )

    assert is_equal(Calculator_Eval("pow($e, 3.8)"), Calculator_Eval("$e^3.8"))
    assert is_equal(Calculator_Eval("pow($e, 3.8)"), Calculator_Eval("exp(3.8)"))
    assert is_equal(Calculator_Eval("mod($pi, $e)"), Calculator_Eval("$pi mod $e"))

    for e, r in test:
        assert is_equal(Calculator_Eval(e), r, e)

def test_mod_operator(Calculator_Eval):
    assert is_equal(Calculator_Eval(".4mod.5"), 0.4)
    assert is_equal(Calculator_Eval("4mod mod(5,3)"), 0)
    assert is_equal(Calculator_Eval("4 mod 5 mod 3"), 1)
    assert is_equal(Calculator_Eval("4 mod pow(2,3) mod 3"), 1)

def test_tuple(Calculator_Xrun):
    case = (
        ("(3,4)", "([3,4])"),
        ("$x:$ans", "(3,4)"),
        ("log(3,4)", "log([3,4])"),
        ("log $x", "log(3,4)"),
        ("mod(3,4)", "mod([3,4])"),
        ("mod $x", "mod(3,4)"),
        ("pow(3,4)", "pow([3,4])"),
        ("pow $x", "pow(3,4)"),
        ("yroot(3,4)", "yroot([3,4])"),
        ("yroot $x", "yroot(3,4)"),
        ("avg(3,4)", "avg([3,4])"),
        ("avg $x", "avg(3,4)"),
        ("sum(3,4)", "sum([3,4])"),
        ("sum $x", "sum(3,4)"),
        ("var(3,4)", "var([3,4])"),
        ("var $x", "var(3,4)"),
        ("varp(3,4)", "varp([3,4])"),
        ("varp $x", "varp(3,4)"),
        ("stdev(3,4)", "stdev([3,4])"),
        ("stdev $x", "stdev(3,4)"),
        ("stdevp(3,4)", "stdevp([3,4])"),
        ("stdevp $x", "stdevp(3,4)"),
        ("$x:tuple(2)", "$ans"),
        ("sin(2)", "sin((2))"),
        ("sin $x", "sin($x)"),
        ("cos(2)", "cos((2))"),
        ("cos $x", "cos($x)"),
        ("tan(2)", "tan((2))"),
        ("tan $x", "tan($x)"),
        ("arcsin(2)", "arcsin((2))"),
        ("arcsin $x", "arcsin($x)"),
        ("arccos(2)", "arccos((2))"),
        ("arccos $x", "arccos($x)"),
        ("arctan(2)", "arctan((2))"),
        ("arctan $x", "arctan($x)"),
        ("sinh(2)", "sinh((2))"),
        ("sinh $x", "sinh($x)"),
        ("cosh(2)", "cosh((2))"),
        ("cosh $x", "cosh($x)"),
        ("tanh(2)", "tanh((2))"),
        ("tanh $x", "tanh($x)"),
        ("log10(2)", "log10((2))"),
        ("log10 $x", "log10($x)"),
        ("ln(2)", "ln((2))"),
        ("ln $x", "ln($x)"),
        ("exp(2)", "exp((2))"),
        ("exp $x", "exp($x)"),
        ("fact(2)", "fact((2))"),
        ("fact $x", "fact($x)"),
        ("sqrt(2)", "sqrt((2))"),
        ("sqrt $x", "sqrt($x)"),
        ("cuberoot(2)", "cuberoot((2))"),
        ("cuberoot $x", "cuberoot($x)"),
        ("avg(2)", "avg((2))"),
        ("avg $x", "avg($x)"),
        ("sum(2)", "sum((2))"),
        ("sum $x", "sum($x)"),
        ("var(2)", "var((2))"),
        ("var $x", "var($x)"),
        ("varp(2)", "varp((2))"),
        ("varp $x", "varp($x)"),
        ("stdev(2)", "stdev((2))"),
        ("stdev $x", "stdev($x)"),
        ("stdevp(2)", "stdevp((2))"),
        ("stdevp $x", "stdevp($x)"),
    )

    for a,b in case:
        assert Calculator_Xrun(a) == Calculator_Xrun(b)

def main():
    pytest.main("-x '%s'" % sys.argv[0])

if __name__ == '__main__':
    main()
