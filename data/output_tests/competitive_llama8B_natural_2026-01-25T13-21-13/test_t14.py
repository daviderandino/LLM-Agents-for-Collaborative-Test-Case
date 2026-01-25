import pytest
from data.input_code.t14 import *

def test_find_Volume_happy_path():
    assert find_Volume(10, 5, 3) == 75.0


def test_find_Volume_zero_length():
    assert find_Volume(0, 5, 3) == 0.0

def test_find_Volume_zero_breadth():
    assert find_Volume(10, 0, 3) == 0.0

def test_find_Volume_negative_dimensions():
    assert find_Volume(-10, -5, -3) == -75.0




def test_find_Volume_mixed_input_types():
    assert find_Volume(10, 5.2, 3) == 78.0

def test_find_Volume_non_numeric_input():
    with pytest.raises(TypeError):
        find_Volume("10", 5, 3)