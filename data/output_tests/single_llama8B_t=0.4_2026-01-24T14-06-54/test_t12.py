import pytest
from data.input_code.t12 import sort_matrix

def test_sort_matrix_success():
    # Test a 2x2 matrix
    M = [[1, 2], [3, 4]]
    expected = [[1, 2], [3, 4]]
    assert sort_matrix(M) == expected

    # Test a 3x3 matrix
    M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert sort_matrix(M) == expected

def test_sort_matrix_empty_matrix():
    # Test an empty matrix
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_single_row_matrix():
    # Test a matrix with a single row
    M = [[1, 2, 3]]
    expected = [[1, 2, 3]]
    assert sort_matrix(M) == expected

def test_sort_matrix_sorted_matrix():
    # Test a matrix that is already sorted
    M = [[1, 2], [3, 4]]
    expected = [[1, 2], [3, 4]]
    assert sort_matrix(M) == expected




def test_sort_matrix_large_matrix():
    # Test a large matrix
    M = [[i + j * 10 for i in range(10)] for j in range(10)]
    expected = [[i + j * 10 for i in range(10)] for j in range(10)]
    assert sort_matrix(M) == expected