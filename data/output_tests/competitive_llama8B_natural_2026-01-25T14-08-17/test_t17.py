import pytest
from data.input_code.t17 import *

def test_square_perimeter_positive():
    assert square_perimeter(5) == 20.0

def test_square_perimeter_zero():
    assert square_perimeter(0) == 0.0




def test_square_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)

def test_square_perimeter_float():
    assert square_perimeter(3.5) == 14.0


def test_square_perimeter_none_type():
    with pytest.raises(TypeError):
        square_perimeter(None)