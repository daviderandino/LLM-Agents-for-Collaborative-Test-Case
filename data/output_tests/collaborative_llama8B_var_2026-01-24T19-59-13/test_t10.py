import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([10, 5, 8, 3, 1], 3, [1, 3, 5]),
    ([10, 5, 8, 3, 1], 0, []),
    ([10, 5, 8, 3, 1], 5, [1, 3, 5, 8, 10]),
    ([], 3, []),
    ([10, 5, 8, 3, 1], -3, []),
])
def test_small_nnum_success(list1, n, expected):
    assert small_nnum(list1, n) == expected

def test_small_nnum_error_non_list():
    with pytest.raises(TypeError):
        small_nnum(None, 3)





def test_small_nnum_error_empty_list():
    with pytest.raises(TypeError):
        small_nnum([], 'three')



