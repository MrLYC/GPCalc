# coding: UTF-8
# Name: Grape单元测试
# Author: LYC
# Created: 2014-04-07

import sys
import pytest
import grape
import random
import math

@pytest.fixture
def Grape():
    return grape.Grape

def test_grape_as_float(Grape):
    a = 0.2
    b = 1.7
    da = Grape(a)
    db = Grape(b)

    assert da == a
    assert da + db == a + b
    assert da - db == a - b
    assert da * db == a * b
    assert da / db == a / b
    assert da % db == a % b
    assert da ** db == a ** b

    assert db == b
    assert db + da == b + a
    assert db - da == b - a
    assert db * da == b * a
    assert db / da == b / a
    assert db % da == b % a
    assert db ** da == b ** a

    assert b + da == db + a
    assert b - da == db - a
    assert b * da == db * a
    assert b / da == db / a
    assert b % da == db % a
    assert b ** da == db ** a

    assert db + a == b + da
    assert db - a == b - da
    assert db * a == b * da
    assert db / a == b / da
    assert db % a == b % da
    assert db ** a == b ** da

def test_grape_as_int(Grape):
    a = 2
    b = 7
    da = Grape(a)
    db = Grape(b)

    assert da == a
    assert da + db == a + b
    assert da - db == a - b
    assert da * db == a * b
    assert int(da / db) == a / b
    assert da % db == a % b
    assert da ** db == a ** b

    assert db == b
    assert db + da == b + a
    assert db - da == b - a
    assert db * da == b * a
    assert int(db / da) == b / a
    assert db % da == b % a
    assert db ** da == b ** a

    assert b + da == db + a
    assert b - da == db - a
    assert b * da == db * a
    assert b / da == db / a
    assert b % da == db % a
    assert b ** da == db ** a

    assert db + a == b + da
    assert db - a == b - da
    assert db * a == b * da
    assert db / a == b / da
    assert db % a == b % da
    assert db ** a == b ** da

def test_grape_as_complex(Grape):
    a = 2.2
    b = 7.7j
    da = Grape("2.2")

    assert b + da == b + a
    assert b - da == b - a
    assert b * da == b * a
    assert b / da == b / a
    assert b % da == b % a
    assert b ** da == b ** a

    assert b + a == b + da
    assert b - a == b - da
    assert b * a == b * da
    assert b / a == b / da
    assert b % a == b % da
    assert b ** a == b ** da

def test_grape_in_tuple(Grape):
    assert (Grape("0.2"), Grape(5)) == (0.2, 5)

def main():
    pytest.main("-x '%s'" % sys.argv[0])

if __name__ == '__main__':
    main()
