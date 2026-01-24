import pytest
from data.input_code.t10 import small_nnum

def test_small_nnum_empty_list():
    assert small_nnum([], 5) == []


def test_small_nnum_none_input():
    with pytest.raises(TypeError):
        small_nnum(None, 5)

def test_small_nnum_zero_n():
    assert small_nnum([1, 2, 3, 4, 5], 0) == []

def test_small_nnum_n_larger_than_list_length():
    assert small_nnum([1, 2, 3, 4, 5], 10) == [1, 2, 3, 4, 5]

def test_small_nnum_n_equal_to_list_length():
    assert small_nnum([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]

def test_small_nnum_n_smaller_than_list_length():
    assert small_nnum([1, 2, 3, 4, 5], 3) == [1, 2, 3]


def test_small_nnum_non_integer_n():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3, 4, 5], 3.5)


def test_small_nnum_list_with_zero():
    assert small_nnum([0, 1, 2, 3, 4], 3) == [0, 1, 2]

def test_small_nnum_list_with_duplicates():
    assert small_nnum([1, 2, 2, 3, 3, 3], 3) == [1, 2, 2]