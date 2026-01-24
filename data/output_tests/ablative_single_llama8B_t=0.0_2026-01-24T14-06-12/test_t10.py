import pytest
from data.input_code.t10 import small_nnum

def test_small_nnum_success():
    # Test with a list of integers
    assert small_nnum([5, 2, 8, 12, 3], 3) == [2, 3, 5]

def test_small_nnum_empty_list():
    # Test with an empty list
    assert small_nnum([], 3) == []

def test_small_nnum_zero_n():
    # Test with n equal to 0
    assert small_nnum([5, 2, 8, 12, 3], 0) == []


def test_small_nnum_large_n():
    # Test with n larger than list length
    assert small_nnum([5, 2, 8, 12, 3], 10) == [2, 3, 5, 8, 12]

def test_small_nnum_none_list():
    # Test with None as input
    with pytest.raises(TypeError):
        small_nnum(None, 3)

def test_small_nnum_none_n():
    # Test with None as n
    with pytest.raises(TypeError):
        small_nnum([5, 2, 8, 12, 3], None)