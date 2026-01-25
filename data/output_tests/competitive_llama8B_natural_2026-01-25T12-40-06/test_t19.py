import pytest
from data.input_code.t19 import *

def test_is_duplicate_no_duplicates():
    assert not is_duplicate([1, 2, 3, 4, 5])

def test_is_duplicate_with_duplicates():
    assert is_duplicate([1, 2, 3, 4, 4])

def test_is_duplicate_empty_array():
    assert not is_duplicate([])

def test_is_duplicate_single_element():
    assert not is_duplicate([1])

def test_is_duplicate_all_negative_numbers():
    assert not is_duplicate([-1, -2, -3, -4, -5])

def test_is_duplicate_all_positive_numbers():
    assert not is_duplicate([1, 2, 3, 4, 5])

    # Explanation: The function is_duplicate checks for duplicates by comparing the length of the input array with the length of a set created from the array.
    # Since None is not equal to any other value, it will be treated as a unique element, resulting in a duplicate when compared with other elements.

    # Explanation: The function is_duplicate checks for duplicates by comparing the length of the input array with the length of a set created from the array.
    # Since float values are not equal to each other, they will be treated as unique elements, resulting in a duplicate when compared with other elements.

    # Explanation: The function is_duplicate checks for duplicates by comparing the length of the input array with the length of a set created from the array.
    # Since 'a' is not equal to any other value, it will be treated as a unique element, resulting in a duplicate when compared with other elements.

def test_is_duplicate_with_duplicates_and_none():
    assert is_duplicate([1, 2, None, 4, 4])  # Expected to return True because None and 4 are duplicates

def test_is_duplicate_with_duplicates_and_float():
    assert is_duplicate([1.1, 2.2, 3.3, 4.4, 4.4])  # Expected to return True because 4.4 is a duplicate

def test_is_duplicate_with_duplicates_and_mixed_data_types():
    assert is_duplicate([1, 'a', 3, 4, 4])  # Expected to return True because 4 is a duplicate