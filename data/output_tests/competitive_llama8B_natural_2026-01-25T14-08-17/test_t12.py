import pytest
from data.input_code.t12 import *

def test_sort_matrix_happy_path():
    M = [[3, 5], [1, 2]]
    expected = [[1, 2], [3, 5]]
    assert sort_matrix(M) == expected

def test_sort_matrix_tie_handling():
    M = [[3, 3], [1, 2]]
    expected = [[1, 2], [3, 3]]
    assert sort_matrix(M) == expected

def test_sort_matrix_duplicate_rows():
    M = [[3, 5], [5, 3]]
    expected = [[3, 5], [5, 3]]
    assert sort_matrix(M) == expected

def test_sort_matrix_more_than_2_rows():
    M = [[3, 5, 1], [10, 2, 3], [4, 6, 2]]
    expected = [[3, 5, 1], [4, 6, 2], [10, 2, 3]]
    assert sort_matrix(M) == expected

def test_sort_matrix_row_with_zeros():
    M = [[3, 5], [0, 0], [1, 2]]
    expected = [[0, 0], [1, 2], [3, 5]]
    assert sort_matrix(M) == expected

def test_sort_matrix_empty_matrix():
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_non_numeric_value():
    M = [[3, 'a'], [1, 2]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_non_list_value():
    M = [3, 5, 1]
    with pytest.raises(TypeError):
        sort_matrix(M)