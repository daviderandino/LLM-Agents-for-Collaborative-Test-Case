import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3], [1, 4, 9]),
    ([-1, -2, -3], [1, 4, 9]),
    ([0, 0, 0], [0, 0, 0]),
    ([1, -2, 3, -4], [1, 4, 9, 16]),
    ([], []),
    ([1.5, 2.5, 3.5], [2.25, 6.25, 12.25]),
])
def test_square_nums_success(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_error_non_integer():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3])

def test_square_nums_error_non_list():
    with pytest.raises(TypeError):
        square_nums({'a': 1, 'b': 2})

def test_square_nums_error_single_element():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3])  # This test case is not necessary, it will fail because of the previous test case
    # Instead, we can test with a single element that is not a list
    with pytest.raises(TypeError):
        square_nums(5)