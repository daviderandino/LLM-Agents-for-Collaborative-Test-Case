import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([], []),
    ([5], [25]),
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
])
def test_square_nums_success(nums, expected):
    result = square_nums(nums)
    assert result == expected

def test_square_nums_none():
    with pytest.raises(TypeError):
        square_nums(None)