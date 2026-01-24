import pytest

from data.input_code.t19 import is_duplicate

def test_test_duplicate_min_length():
    result = is_duplicate([1, 2, 3, 1])
    assert result == True

def test_test_duplicate_max_length():
    result = is_duplicate([1, 1, 1, 1, 1])
    assert result == True

def test_test_duplicate_no_duplicates():
    result = is_duplicate([1, 2, 3, 4])
    assert result == False

def test_test_duplicate_empty_array():
    result = is_duplicate([])
    assert result == False

def test_test_duplicate_none_input():
    with pytest.raises(TypeError):
        is_duplicate(None)




def test_test_duplicate_non_list():
    with pytest.raises(TypeError):
        is_duplicate(123)