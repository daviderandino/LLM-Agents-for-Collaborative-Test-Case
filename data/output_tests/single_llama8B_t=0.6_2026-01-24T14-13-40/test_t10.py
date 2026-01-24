import pytest
from data.input_code.t10 import small_nnum

def test_small_nnum_valid_input():
    list1 = [5, 3, 8, 2, 9]
    n = 3
    result = small_nnum(list1, n)
    assert result == [2, 3, 5]

def test_small_nnum_edge_case_n_zero():
    list1 = [5, 3, 8, 2, 9]
    n = 0
    result = small_nnum(list1, n)
    assert result == []

def test_small_nnum_edge_case_n_greater_than_list_length():
    list1 = [5, 3, 8, 2, 9]
    n = 10
    result = small_nnum(list1, n)
    assert result == [2, 3, 5, 8, 9]

def test_small_nnum_empty_list():
    list1 = []
    n = 3
    result = small_nnum(list1, n)
    assert result == []

def test_small_nnum_list_with_duplicates():
    list1 = [5, 5, 3, 8, 2, 9]
    n = 3
    result = small_nnum(list1, n)
    assert result == [2, 3, 5]

def test_small_nnum_none_input():
    list1 = None
    n = 3
    with pytest.raises(TypeError):
        small_nnum(list1, n)

