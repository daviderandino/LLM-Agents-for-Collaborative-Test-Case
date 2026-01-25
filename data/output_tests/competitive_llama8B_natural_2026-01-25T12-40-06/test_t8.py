import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3], [1, 4, 9]),
    ([-1, -2, -3], [1, 4, 9]),
    ([0, 0, 0], [0, 0, 0]),
    ([], []),
    ("hello", TypeError)
])
def test_square_nums(nums, expected):
    if isinstance(expected, type):
        with pytest.raises(expected):
            square_nums(nums)
    else:
        assert square_nums(nums) == expected

def test_square_nums_single_element():
    assert square_nums([5]) == [25]

def test_square_nums_large_number():
    assert square_nums([1000000]) == [1000000000000]

def test_square_nums_float_number():
    assert square_nums([1.5]) == [2.25]