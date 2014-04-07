# coding: UTF-8
# Name: Gray单元测试
# Author: LYC
# Created: 2014-04-07

import sys
import pytest
import gray
import random
import math

@pytest.fixture
def Gray():
    return gray.Gray

def test_gray_as_float(Gray):
    a = 0.2
    b = 1.7
    da = Gray(a)
    db = Gray(b)

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

def test_gray_as_int(Gray):
    a = 2
    b = 7
    da = Gray(a)
    db = Gray(b)

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

def test_gray_as_complex(Gray):
    a = 2.2
    b = 7.7j
    da = Gray("2.2")

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

def test_gray_in_tuple(Gray):
    assert (Gray("0.2"), Gray(5)) == (0.2, 5)

def main():
    pytest.main("-x '%s'" % sys.argv[0])

if __name__ == '__main__':
    main()
