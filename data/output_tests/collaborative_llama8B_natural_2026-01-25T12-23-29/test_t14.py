import pytest
from data.input_code.t14 import *



def test_find_Volume_non_zero():
    assert find_Volume(5, 2, 3) == ((5 * 2 * 3) / 2)  # Test with non-zero parameters

def test_find_Volume_zero_length():
    assert find_Volume(0, 2, 3) == 0  # Test with zero length

def test_find_Volume_zero_base():
    assert find_Volume(5, 0, 3) == 0  # Test with zero base

def test_find_Volume_zero_height():
    assert find_Volume(5, 2, 0) == 0  # Test with zero height