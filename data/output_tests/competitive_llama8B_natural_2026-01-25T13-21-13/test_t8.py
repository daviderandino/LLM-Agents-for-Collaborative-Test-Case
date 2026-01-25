import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([], [])
])
def test_square_nums_empty_input(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5], [25]),
    ([0], [0])
])
def test_square_nums_single_positive_or_zero(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5], [25]),
    ([0], [0])
])
def test_square_nums_single_negative(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]),
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
])
def test_square_nums_list_of_positive_numbers(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]),
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
])
def test_square_nums_list_of_negative_numbers(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 0, 3, 4], [1, 4, 0, 9, 16]),
    ([1, 2, 0, 3, 4], [1, 4, 0, 9, 16])
])
def test_square_nums_list_of_mixed_numbers(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_list_with_non_numeric_values():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3, 4, 5])

def test_square_nums_list_with_single_non_numeric_value():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3])

def test_square_nums_list_with_none():
    with pytest.raises(TypeError):
        square_nums([1, None, 3])