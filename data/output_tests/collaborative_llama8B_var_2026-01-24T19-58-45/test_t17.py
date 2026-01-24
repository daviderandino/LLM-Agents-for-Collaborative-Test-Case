import pytest
from data.input_code.t17 import *



def test_square_perimeter_zero():
    result = square_perimeter(0)
    assert result == 0

