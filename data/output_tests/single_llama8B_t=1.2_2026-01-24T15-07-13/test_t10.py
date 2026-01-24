import pytest
from data.input_code.t10 import small_nnum

# Test Function small_nnum() to check for positive input.
def test_small_nnum_positive():
    # Arrange
    list1 = [5, 3, 8, 2, 1, 4, 6, 7, 9]
    n = 3
    # Act
    result = small_nnum(list1, n)
    # Assert
    assert result == [1, 2, 3]

# Test Function small_nnum() with empty list, edge case.
def test_small_nnum_empty_list():
    # Arrange
    list1 = []
    n = 3
    # Act
    result = small_nnum(list1, n)
    # Assert
    assert result == []

# Test Function small_nnum()  n greater than list length.
def test_small_nnum_n_greater_than_list_length():
    # Arrange
    list1 = [4, 5, 2, 8, 5, 6]
    n = 7
    # Act
    result = small_nnum(list1, n)
    # Assert
    expected = sorted(list1)[:7]
    assert result == expected

# Test exception is not raised for valid n values.
def test_small_nnum_no_exception():
    # Arrange
    list1 = [4, 8, 7, 1, 6]
    n = 5
    # Act and assert no exception raised
    result = small_nnum(list1, n)
    assert result == [1, 4, 6, 7, 8]

# Test Function small_nnum() to check for non positive n input and throw error.
