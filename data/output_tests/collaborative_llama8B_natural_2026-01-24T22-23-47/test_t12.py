import pytest
from data.input_code.t12 import *

@pytest.mark.parametrize('M, expected', [
    ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
])
def test_sort_matrix_success(M, expected):
    assert sort_matrix(M) == expected

def test_sort_matrix_duplicate_rows():
    assert sort_matrix([[1, 2, 3], [1, 2, 3], [4, 5, 6]]) == [[1, 2, 3], [1, 2, 3], [4, 5, 6]]

def test_sort_matrix_non_numeric_values():
    with pytest.raises(TypeError):
        sort_matrix([[1, 2, 'a'], [4, 5, 6]])

def test_sort_matrix_empty_matrix():
    assert sort_matrix([]) == []

def test_sort_matrix_single_row():
    assert sort_matrix([[1, 2, 3]]) == [[1, 2, 3]]

def test_sort_matrix_single_column():
    with pytest.raises(ValueError):
        sort_matrix([[1], [2], [3]])

# The issue with the original test is that it expected a ValueError to be raised when sorting a single column matrix.
# However, the sort_matrix function does not check for this case. It simply sorts the matrix based on the sum of its rows.
# Therefore, the correct test should not expect a ValueError to be raised.

# The correct test for the sort_matrix function is to check if it correctly sorts the matrix based on the sum of its rows.
# Since the sum of the rows in a single column matrix is the same for all rows, the function will not be able to sort the matrix.
# Therefore, the correct test should check if the function returns the original matrix when given a single column matrix.

def test_sort_matrix_single_column():
    assert sort_matrix([[1], [2], [3]]) == [[1], [2], [3]]