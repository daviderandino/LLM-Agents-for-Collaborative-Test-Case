import pytest
from data.input_code.t17 import *



def test_square_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)


def test_square_perimeter_zero():
    assert square_perimeter(0) == 0  # This test case is correct, the perimeter of a square with side length 0 is indeed 0