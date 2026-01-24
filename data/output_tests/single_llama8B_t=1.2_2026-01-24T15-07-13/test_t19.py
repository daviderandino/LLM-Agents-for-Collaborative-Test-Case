import pytest

from data.input_code.t19 import test_duplicate

def test_test_duplicate_min_length():
    result = test_duplicate([1, 2, 3, 1])
    assert result == True

def test_test_duplicate_max_length():
    result = test_duplicate([1, 1, 1, 1, 1])
    assert result == True

def test_test_duplicate_no_duplicates():
    result = test_duplicate([1, 2, 3, 4])
    assert result == False

def test_test_duplicate_empty_array():
    result = test_duplicate([])
    assert result == False

def test_test_duplicate_none_input():
    with pytest.raises(TypeError):
        test_duplicate(None)




def test_test_duplicate_non_list():
    with pytest.raises(TypeError):
        test_duplicate(123)