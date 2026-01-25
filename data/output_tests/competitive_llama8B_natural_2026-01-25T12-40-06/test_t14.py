import pytest
from data.input_code.t14 import *


def test_find_Volume_zero_result():
    assert find_Volume(0, 0, 4) == 0.0

def test_find_Volume_float_input():
    assert isinstance(find_Volume(5.5, 3.7, 4.2), float)

def test_find_Volume_large_input():
    assert isinstance(find_Volume(1000, 500, 200), float)


