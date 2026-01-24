import pytest
from data.input_code.t8 import square_nums

def test_square_nums_empty_list():
    assert square_nums([]) == []

def test_square_nums_single_element():
    assert square_nums([5]) == [25]

def test_square_nums_multiple_elements():
    assert square_nums([5, 3, 7]) == [25, 9, 49]


