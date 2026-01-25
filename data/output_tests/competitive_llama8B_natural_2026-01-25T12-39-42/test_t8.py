import pytest
from data.input_code.t8 import *

def test_square_nums_empty_list():
    assert square_nums([]) == []

def test_square_nums_single_element():
    assert square_nums([5]) == [25]

def test_square_nums_multiple_elements():
    assert square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]

def test_square_nums_non_numeric_input():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3, 4, 5])

def test_square_nums_large_numbers():
    assert square_nums([2**100, 2**100]) == [2**200, 2**200]

def test_square_nums_negative_numbers():
    assert square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25]