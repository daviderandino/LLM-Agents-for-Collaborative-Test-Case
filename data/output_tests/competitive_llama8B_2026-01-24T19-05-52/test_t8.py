import pytest
from data.input_code.t8 import *

def test_square_nums():
    assert square_nums([]) == []

def test_square_nums_single_num():
    assert square_nums([5]) == [25]

def test_square_nums_multiple_nums():
    assert square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]

def test_square_nums_negative_nums():
    assert square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25]

def test_square_nums_zero():
    assert square_nums([0]) == [0]

def test_square_nums_string_input():
    with pytest.raises(TypeError):
        square_nums('a')

def test_square_nums_mixed_input():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3, 4, 5])