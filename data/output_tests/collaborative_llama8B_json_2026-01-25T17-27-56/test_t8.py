import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([], []),
    ([5], [25]),
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]),
])
def test_square_nums_success(nums, expected):
    assert square_nums(nums) == expected

def test_square_nums_none():
    with pytest.raises(TypeError):
        square_nums(None)

def test_square_nums_zero():
    assert square_nums([0]) == [0]