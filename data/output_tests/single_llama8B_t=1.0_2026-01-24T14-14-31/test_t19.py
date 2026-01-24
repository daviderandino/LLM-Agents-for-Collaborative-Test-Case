import pytest

from data.input_code.t19 import is_duplicate

def test_duplicate_success():
    # Test case with duplicate numbers in the array
    assert is_duplicate([1, 2, 3, 2, 1]) == True

def test_duplicate_no_duplicates():
    # Test case with no duplicates in the array
    assert is_duplicate([1, 2, 3, 4, 5]) == False

def test_duplicate_empty_array():
    # Test case with an empty array
    assert is_duplicate([]) == False

def test_duplicate_single_element_array():
    # Test case with an array containing a single element
    assert is_duplicate([1]) == False

def test_duplicate_negative_numbers():
    # Test case with an array containing negative numbers
    assert is_duplicate([-1, 1, -1]) == True

def test_duplicate_zeros():
    # Test case with an array containing zeros
    assert is_duplicate([0, 0, 0]) == True

def test_duplicate_floats():
    # Test case with an array containing floats
    assert is_duplicate([1.0, 2.0, 2.0]) == True

def test_duplicate_large_array():
    # Test case with a large array containing duplicates
    assert is_duplicate(list(range(100)) + list(range(100, 0, -1))) == True