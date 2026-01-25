import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]),
    ([-1, -2, -3, -4, -5], [1, 4, 9, 16, 25]),
    ([0, 2, 3, 4, 5], [0, 4, 9, 16, 25]),
    ([], []),
    ([5], [25])
])
def test_square_nums_success(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_empty_list():
    assert square_nums([]) == []

def test_square_nums_single_element():
    assert square_nums([5]) == [25]

def test_square_nums_non_iterable():
    with pytest.raises(TypeError):
        square_nums(None)

def test_square_nums_non_numeric():
    with pytest.raises(TypeError):
        square_nums(['a', 'b', 'c'])

def test_square_nums_mixed_types():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3, 4, 5])