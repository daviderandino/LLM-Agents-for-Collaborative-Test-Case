import pytest
from data.input_code.t10 import small_nnum
import heapq


def test_small_nnum_empty_list():
    # Test with an empty list
    assert small_nnum([], 3) == []

def test_small_nnum_n_zero():
    # Test with n equal to zero
    assert small_nnum([5, 2, 8, 12, 3], 0) == []

def test_small_nnum_n_larger_than_list():
    # Test with n larger than the list length
    assert small_nnum([5, 2, 8, 12, 3], 10) == [2, 3, 5, 8, 12]

