import pytest
from data.input_code.t12 import *

def test_sort_matrix_happy_path_small_matrix():
    M = [[1, 2], [3, 4]]
    expected = [[1, 2], [3, 4]]
    assert sort_matrix(M) == expected

def test_sort_matrix_happy_path_larger_matrix():
    M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert sort_matrix(M) == expected


def test_sort_matrix_type_mismatch():
    M = [[1, 2, 'a'], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_type_mismatch_none():
    M = [[1, 2, None], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_empty_matrix():
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_single_row_matrix():
    M = [[1, 2, 3]]
    expected = [[1, 2, 3]]
    assert sort_matrix(M) == expected


