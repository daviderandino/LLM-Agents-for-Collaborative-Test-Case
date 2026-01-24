import pytest

from data.input_code.t17 import square_perimeter


def test_square_perimeter_zero():
    assert square_perimeter(0) == 0

def test_square_perimeter_isinstance():
    assert square_perimeter("a") != None