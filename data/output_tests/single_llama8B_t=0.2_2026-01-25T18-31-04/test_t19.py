import pytest

from data.input_code.t19 import is_duplicate

def test_is_duplicate_success():
    # Test case with duplicate elements
    assert is_duplicate([1, 2, 3, 2]) == True

def test_is_duplicate_no_duplicates():
    # Test case with no duplicate elements
    assert is_duplicate([1, 2, 3, 4]) == False

def test_is_duplicate_empty_array():
    # Test case with an empty array
    assert is_duplicate([]) == False

def test_is_duplicate_single_element():
    # Test case with a single element array
    assert is_duplicate([1]) == False

def test_is_duplicate_none_input():
    # Test case with None input
    with pytest.raises(TypeError):
        is_duplicate(None)

