import pytest
from data.input_code.t10 import small_nnum

def test_small_nnum_success():
    list1 = [5, 2, 9, 1, 7, 3]
    n = 3
    expected_output = [1, 2, 3]
    assert small_nnum(list1, n) == expected_output

def test_small_nnum_empty_list():
    list1 = []
    n = 3
    expected_output = []
    assert small_nnum(list1, n) == expected_output

def test_small_nnum_zero_n():
    list1 = [5, 2, 9, 1, 7, 3]
    n = 0
    expected_output = []
    assert small_nnum(list1, n) == expected_output



def test_small_nnum_none_list():
    list1 = None
    n = 3
    with pytest.raises(TypeError):
        small_nnum(list1, n)

def test_small_nnum_none_n():
    list1 = [5, 2, 9, 1, 7, 3]
    n = None
    with pytest.raises(TypeError):
        small_nnum(list1, n)