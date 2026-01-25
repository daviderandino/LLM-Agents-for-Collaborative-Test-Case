import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([3, 5, 1, 2, 4], 3, [1, 2, 3]),
    ([10, 20, 30, 40, 50], 2, [10, 20]),
])
def test_small_nnum_success(list1, n, expected):
    assert small_nnum(list1, n) == expected

def test_small_nnum_edge_n_zero():
    assert small_nnum([10, 20, 30, 40, 50], 0) == []

def test_small_nnum_edge_n_equal_list_length():
    assert small_nnum([10, 20, 30, 40, 50], 5) == [10, 20, 30, 40, 50]