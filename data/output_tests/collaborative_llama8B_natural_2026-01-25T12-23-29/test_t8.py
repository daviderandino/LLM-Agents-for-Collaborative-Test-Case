import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([], [])
])
def test_square_nums_empty_list(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([5], [25]),
    ([10], [100]),
])
def test_square_nums_single_element(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3], [1, 4, 9]),
    ([4, 5, 6], [16, 25, 36]),
])
def test_square_nums_multiple_elements(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([-1, -2, -3], [1, 4, 9]),
    ([-4, -5, -6], [16, 25, 36]),
])
def test_square_nums_negative_numbers(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_non_numeric_values():
    with pytest.raises(TypeError):
        square_nums(['a', 'b', 'c'])

@pytest.mark.parametrize('nums, expected', [
    ([1.5, 2.5, 3.5], [2.25, 6.25, 12.25]),
    ([4.5, 5.5, 6.5], [20.25, 30.25, 42.25]),
])
def test_square_nums_float_numbers(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_zero():
    assert square_nums([0, 5, 10]) == [0, 25, 100]

@pytest.mark.parametrize('nums, expected', [
    ([i for i in range(1000)], [i**2 for i in range(1000)]),
])
def test_square_nums_large_list(nums, expected):
    assert square_nums(nums) == expected