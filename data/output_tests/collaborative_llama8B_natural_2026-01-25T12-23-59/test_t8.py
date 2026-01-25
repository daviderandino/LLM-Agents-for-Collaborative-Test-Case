import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3], [1, 4, 9]),
    ([-1, -2, -3], [1, 4, 9]),
    ([0, 0, 0], [0, 0, 0]),
    ([], []),
    ([5], [25])
])
def test_square_nums_success(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_zero_handling():
    assert square_nums([0, 0, 0]) == [0, 0, 0]

def test_square_nums_empty_list():
    assert square_nums([]) == []

def test_square_nums_single_element_list():
    assert square_nums([5]) == [25]

def test_square_nums_non_numeric_input():
    with pytest.raises(TypeError):
        square_nums(['a', 2, 3])

def test_square_nums_non_list_input():
    with pytest.raises(TypeError):
        square_nums({'a': 1})

def test_square_nums_non_iterable_input():
    with pytest.raises(TypeError):
        square_nums(True)