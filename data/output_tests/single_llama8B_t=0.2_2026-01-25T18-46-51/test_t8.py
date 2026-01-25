import pytest

from data.input_code.t8 import square_nums

def test_square_nums_empty_list():
    assert square_nums([]) == []

def test_square_nums_single_element():
    assert square_nums([5]) == [25]

def test_square_nums_multiple_elements():
    assert square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]

def test_square_nums_negative_numbers():
    assert square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25]

def test_square_nums_zero():
    assert square_nums([0]) == [0]

def test_square_nums_none():
    with pytest.raises(TypeError):
        square_nums(None)