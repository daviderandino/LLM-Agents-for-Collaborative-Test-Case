import pytest

from data.input_code.t17 import square_perimeter

def test_square_perimeter_positive(a):
    assert square_perimeter(1) == 4
    assert square_perimeter(2.5) == 10
    assert square_perimeter(10.0) == 40
    assert square_perimeter(100) == 400


def test_square_perimeter_zero():
    assert square_perimeter(0) == 0

def test_square_perimeter_isinstance():
    assert square_perimeter("a") != None