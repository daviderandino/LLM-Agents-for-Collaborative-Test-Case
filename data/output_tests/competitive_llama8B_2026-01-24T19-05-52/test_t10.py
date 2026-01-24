import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([1, 2, 3, 4, 5], 3, [1, 2, 3]),
    ([1, 2, 3, 4, 5], 6, [1, 2, 3, 4, 5]),
    ([1, 2, 3, 4, 5], 0, []),
    ([], 3, []),
    ([1, 2, 3, 4, 5], -3, []),
])
def test_small_nnum_success(list1, n, expected):
    assert small_nnum(list1, n) == expected

def test_small_nnum_error_empty_list():
    with pytest.raises(TypeError):
        small_nnum(None, 3)

def test_small_nnum_error_non_integer_n():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3, 4, 5], 'a')