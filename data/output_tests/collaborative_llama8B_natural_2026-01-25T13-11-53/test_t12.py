import pytest
from data.input_code.t12 import *

def test_sort_matrix_happy_path():
    M = [[1, 2], [3, 4]]
    expected = [[1, 2], [3, 4]]
    assert sort_matrix(M) == expected

def test_sort_matrix_duplicate_rows():
    M = [[1, 2], [1, 2], [3, 4]]
    expected = [[1, 2], [1, 2], [3, 4]]
    assert sort_matrix(M) == expected

def test_sort_matrix_rows_with_different_sums():
    M = [[1, 2], [3, 4], [5, 6]]
    expected = [[1, 2], [3, 4], [5, 6]]
    assert sort_matrix(M) == expected

def test_sort_matrix_empty_matrix():
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_single_row():
    M = [[1, 2]]
    expected = [[1, 2]]
    assert sort_matrix(M) == expected


def test_sort_matrix_non_list_input():
    M = {'a': 1, 'b': 2}
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_non_numeric_values():
    M = [[1, 'a'], [3, 4]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_mixed_numeric_non_numeric_values():
    M = [[1, 2], ['a', 4]]
    with pytest.raises(TypeError):
        sort_matrix(M)


def test_sort_matrix_single_column_sort():
    M = [[1], [2]]
    expected = [[1], [2]]
    assert sort_matrix(M) == expected

