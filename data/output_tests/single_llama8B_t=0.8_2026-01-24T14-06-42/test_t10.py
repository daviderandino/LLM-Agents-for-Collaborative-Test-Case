import pytest
from data.input_code.t10 import small_nnum

def test_small_nnum_empty_list():
    assert small_nnum([], 1) == []

def test_small_nnum_zero_n():
    assert small_nnum([1, 2, 3], 0) == []

def test_small_nnum_positive_n():
    assert small_nnum([1, 2, 3], 1) == [1]

def test_small_nnum_n_larger_than_list():
    assert small_nnum([1, 2, 3], 4) == [1, 2, 3]



def test_small_nnum_non_integer_n():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3], 1.5)

