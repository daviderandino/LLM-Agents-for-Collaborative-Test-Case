import pytest
from data.input_code.t8 import *


def test_square_nums_error():
    with pytest.raises(TypeError):
        square_nums('a')

def test_square_nums_empty_list():
    result = square_nums([])
    assert result == []

def test_square_nums_single_element():
    result = square_nums([5])
    assert result == [25]

def test_square_nums_multiple_elements():
    result = square_nums([1, 2, 3, 4, 5])
    assert result == [1, 4, 9, 16, 25]

def test_square_nums_negative_numbers():
    result = square_nums([-1, -2, -3, -4, -5])
    assert result == [1, 4, 9, 16, 25]

def test_square_nums_zero():
    result = square_nums([0])
    assert result == [0]

def test_square_nums_non_numeric_input():
    with pytest.raises(TypeError):
        square_nums('a')

def test_square_nums_non_numeric_input_2():
    with pytest.raises(TypeError):
        square_nums(['a', 'b', 'c'])