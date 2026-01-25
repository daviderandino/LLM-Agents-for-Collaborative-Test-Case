import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
])
def test_square_nums_success(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([], [])
])
def test_square_nums_empty(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    (None, TypeError)
])
def test_square_nums_none_error(nums, expected):
    with pytest.raises(expected):
        square_nums(nums)

@pytest.mark.parametrize('nums, expected', [
    ([10], [100])
])
def test_square_nums_single(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([1.5, 2.5, 3.5], [2.25, 6.25, 12.25])
])
def test_square_nums_float(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    ([-1, -2, -3], [1, 4, 9])
])
def test_square_nums_negative(nums, expected):
    assert square_nums(nums) == expected

@pytest.mark.parametrize('nums, expected', [
    (['a', 'b', 'c'], TypeError)
])
def test_square_nums_non_numeric_error(nums, expected):
    with pytest.raises(expected):
        square_nums(nums)