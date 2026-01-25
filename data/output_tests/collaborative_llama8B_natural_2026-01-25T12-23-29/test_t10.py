import pytest
from data.input_code.t10 import *


def test_small_nnum_empty_list():
    assert small_nnum([], 2) == []

def test_small_nnum_n_zero():
    assert small_nnum([1, 2, 3], 0) == []


def test_small_nnum_float_input():
    assert small_nnum([1.1, 2.2, 3.3], 2) == [1.1, 2.2]

def test_small_nnum_negative_input():
    assert small_nnum([-1, -2, -3], 2) == [-3, -2]

def test_small_nnum_mixed_input():
    assert small_nnum([-1, 1, -2, 2], 2) == [-2, -1]

def test_small_nnum_duplicates():
    assert small_nnum([1, 2, 2, 3, 3], 2) == [1, 2]

def test_small_nnum_non_numeric_input():
    with pytest.raises(TypeError):
        small_nnum([1, 'a', 2, 3], 2)

def test_small_nnum_non_numeric_input2():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 'a', 3], 2)

def test_small_nnum_non_numeric_input3():
    with pytest.raises(TypeError):
        small_nnum([1, 'a', 2, 'b'], 2)