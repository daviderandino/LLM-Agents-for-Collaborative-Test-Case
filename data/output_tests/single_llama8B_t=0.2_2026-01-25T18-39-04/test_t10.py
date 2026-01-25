import pytest
from data.input_code.t10 import small_nnum

def test_small_nnum_smallest():
    list1 = [5, 2, 8, 12, 3]
    n = 3
    expected = [2, 3, 5]
    assert small_nnum(list1, n) == expected

def test_small_nnum_empty_list():
    list1 = []
    n = 3
    expected = []
    assert small_nnum(list1, n) == expected

def test_small_nnum_zero_n():
    list1 = [5, 2, 8, 12, 3]
    n = 0
    expected = []
    assert small_nnum(list1, n) == expected

def test_small_nnum_large_n():
    list1 = [5, 2, 8, 12, 3]
    n = 10
    expected = [2, 3, 5, 8, 12]
    assert small_nnum(list1, n) == expected


def test_small_nnum_none_list():
    list1 = None
    n = 3
    with pytest.raises(TypeError):
        small_nnum(list1, n)

def test_small_nnum_none_n():
    list1 = [5, 2, 8, 12, 3]
    n = None
    with pytest.raises(TypeError):
        small_nnum(list1, n)