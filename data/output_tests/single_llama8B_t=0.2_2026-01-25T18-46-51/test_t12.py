import pytest
from data.input_code.t12 import sort_matrix


def test_sort_matrix_empty_matrix():
    # Test with an empty matrix
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_single_row_matrix():
    # Test with a matrix containing a single row
    M = [[1, 2, 3]]
    expected = [[1, 2, 3]]
    assert sort_matrix(M) == expected

def test_sort_matrix_single_element_matrix():
    # Test with a matrix containing a single element
    M = [[5]]
    expected = [[5]]
    assert sort_matrix(M) == expected

def test_sort_matrix_invalid_input():
    # Test with invalid input (not a list)
    with pytest.raises(TypeError):
        sort_matrix("not a matrix")


