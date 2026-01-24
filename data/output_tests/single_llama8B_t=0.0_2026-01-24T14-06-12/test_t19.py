import pytest

from data.input_code.t19 import test_duplicate

def test_duplicate_success():
    # Test case with duplicate numbers
    assert test_duplicate([1, 2, 3, 2]) == True

def test_duplicate_no_duplicates():
    # Test case with no duplicate numbers
    assert test_duplicate([1, 2, 3, 4]) == False

def test_duplicate_empty_list():
    # Test case with an empty list
    assert test_duplicate([]) == False

def test_duplicate_single_element_list():
    # Test case with a list containing a single element
    assert test_duplicate([1]) == False

def test_duplicate_none_input():
    # Test case with None input
    with pytest.raises(TypeError):
        test_duplicate(None)

