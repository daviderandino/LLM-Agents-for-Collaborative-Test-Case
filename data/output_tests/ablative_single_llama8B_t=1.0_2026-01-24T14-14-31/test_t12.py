import pytest

from data.input_code.t12 import sort_matrix




def test_sort_matrix_empty_matrix():
    # Test an empty matrix
    matrix = []
    expected = []
    result = sort_matrix(matrix)
    assert result == expected

