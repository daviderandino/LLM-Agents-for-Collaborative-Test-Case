import pytest
from data.input_code.t10 import small_nnum
import heapq

def test_small_nnum_success():
    # Test with a list of integers and n=3
    assert small_nnum([5, 2, 8, 12, 3], 3) == [2, 3, 5]

def test_small_nnum_empty_list():
    # Test with an empty list
    assert small_nnum([], 3) == []

def test_small_nnum_n_zero():
    # Test with n=0
    assert small_nnum([5, 2, 8, 12, 3], 0) == []



def test_small_nnum_non_integer_n():
    # Test with non-integer n
    with pytest.raises(TypeError):
        small_nnum([5, 2, 8, 12, 3], 3.5)

