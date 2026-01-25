import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([], [])
])
def test_square_nums_empty_list(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5], [25]),
    ([0], [0]),
    ([1], [1]),
    ([2], [4]),
    ([3], [9])
])
def test_square_nums_single_positive(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5], [25]),
    ([0], [0]),
    ([1], [1]),
    ([2], [4]),
    ([3], [9])
])
def test_square_nums_single_negative(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5, 0], [25, 0]),
    ([0, 5], [0, 25]),
    ([1, 0], [1, 0]),
    ([0, 1], [0, 1]),
    ([2, 0], [4, 0]),
    ([0, 2], [0, 4]),
    ([3, 0], [9, 0]),
    ([0, 3], [0, 9])
])
def test_square_nums_multiple_positive(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5, -5], [25, 25]),
    ([0, -5], [0, 25]),
    ([1, -5], [1, 25]),
    ([2, -5], [4, 25]),
    ([3, -5], [9, 25])
])
def test_square_nums_multiple_negative(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5, -2, 3], [25, 4, 9]),
    ([1, -2, 3], [1, 4, 9]),
    ([2, -2, 3], [4, 4, 9]),
    ([3, -2, 3], [9, 4, 9])
])
def test_square_nums_mixed_input(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_non_iterable():
    with pytest.raises(TypeError):
        square_nums('hello')

def test_square_nums_non_numeric_values():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3])