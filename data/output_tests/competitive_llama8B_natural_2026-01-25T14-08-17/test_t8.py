import pytest
from data.input_code.t8 import *

def test_square_nums_empty_list():
    assert square_nums([]) == []

def test_square_nums_positive_numbers():
    assert square_nums([1, 2, 3]) == [1, 4, 9]

def test_square_nums_negative_numbers():
    assert square_nums([-1, -2, -3]) == [1, 4, 9]

def test_square_nums_zero_handling():
    assert square_nums([1, 0, 3]) == [1, 0, 9]

def test_square_nums_single_element():
    assert square_nums([5]) == [25]

def test_square_nums_non_numeric_elements():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3])

def test_square_nums_non_list_input():
    with pytest.raises(TypeError):
        square_nums('hello')

def test_square_nums_only_non_numeric_elements():
    with pytest.raises(TypeError):
        square_nums(['a', 'b', 'c'])