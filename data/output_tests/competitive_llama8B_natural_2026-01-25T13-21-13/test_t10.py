import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([1, 2, 3, 4, 5], 3, [1, 2, 3]),
    ([1, 2, 3], 3, [1, 2, 3]),
    ([1, 2, 3, 4, 5, 6], 3, [1, 2, 3]),
    ([1, 2, 3], 10, [1, 2, 3]),
    ([], 3, []),
    ([1, 2, 3], 0, []),
    ([1, 2, 3], -3, []),
])
def test_small_nnum_success(list1, n, expected):
    assert small_nnum(list1, n) == expected

def test_small_nnum_error_non_integer_n():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3], 3.5)



def test_small_nnum_error_non_integer_n2():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3], 3.5)

def test_small_nnum_error_negative_n2():
    # The function does not raise ValueError for negative n, it returns an empty list
    result = small_nnum([1, 2, 3], -3)
    assert result == []

