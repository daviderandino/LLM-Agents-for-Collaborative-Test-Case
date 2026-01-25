import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([1, 2, 3, 4, 5], 3, [1, 2, 3]),
    ([5, 4, 3, 2, 1], 3, [1, 2, 3]),
    ([10, 20, 30, 40, 50], 3, [10, 20, 30]),
    ([5, 2, 8, 1, 9], 3, [1, 2, 5]),
    ([1000000, 2000000, 3000000, 4000000, 5000000], 3, [1000000, 2000000, 3000000]),
])
def test_small_nnum_success(list1, n, expected):
    assert small_nnum(list1, n) == expected

def test_small_nnum_empty_list():
    assert small_nnum([], 3) == []



def test_small_nnum_large_numbers():
    assert small_nnum([1000000, 2000000, 3000000, 4000000, 5000000], 3) == [1000000, 2000000, 3000000]



def test_small_nnum_invalid_n_type():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3], 'a')


def test_small_nnum_non_numeric_data():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 'a', 4, 5], 3)

def test_small_nnum_large_list():
    assert small_nnum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 3) == [1, 2, 3]

