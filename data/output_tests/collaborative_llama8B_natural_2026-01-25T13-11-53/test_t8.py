import pytest
from data.input_code.t8 import *

def test_square_nums_empty_list():
    assert square_nums([]) == []

def test_square_nums_single_positive():
    assert square_nums([5]) == [25]

def test_square_nums_single_negative():
    assert square_nums([-5]) == [25]

def test_square_nums_single_zero():
    assert square_nums([0]) == [0]

def test_square_nums_mixed_numbers():
    assert square_nums([5, -3, 0, 2, -1]) == [25, 9, 0, 4, 1]

def test_square_nums_float_number():
    assert square_nums([4.5]) == [20.25]

def test_square_nums_large_number():
    assert square_nums([1000000]) == [1000000000000]

def test_square_nums_non_numeric_input():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3.5])