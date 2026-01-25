import pytest

from data.input_code.t19 import is_duplicate

def test_is_duplicate_empty_list():
    assert is_duplicate([]) == False

def test_is_duplicate_no_duplicates():
    assert is_duplicate([1, 2, 3, 4, 5]) == False

def test_is_duplicate_duplicates():
    assert is_duplicate([1, 2, 2, 3, 4, 4, 5]) == True

def test_is_duplicate_all_duplicates():
    assert is_duplicate([1, 1, 1, 1, 1]) == True

def test_is_duplicate_single_element():
    assert is_duplicate([1]) == False

def test_is_duplicate_none():
    with pytest.raises(TypeError):
        is_duplicate(None)

