import pytest
from data.input_code.t12 import *


def test_sort_matrix_zero_handling():
    assert sort_matrix([[1, 0], [3, 4]]) == [[1, 0], [3, 4]]

def test_sort_matrix_empty_input():
    assert sort_matrix([]) == []

def test_sort_matrix_single_row():
    assert sort_matrix([[1, 2]]) == [[1, 2]]

def test_sort_matrix_duplicate_rows_same_sum():
    assert sort_matrix([[1, 2], [3, 4], [1, 2]]) == [[1, 2], [1, 2], [3, 4]]

def test_sort_matrix_duplicate_rows_different_sums():
    assert sort_matrix([[1, 2], [3, 4], [5, 6]]) == [[1, 2], [3, 4], [5, 6]]

def test_sort_matrix_large_input():
    assert sort_matrix([[1, 2] for _ in range(10000)]) == [[1, 2] for _ in range(10000)]

def test_sort_matrix_large_columns():
    assert sort_matrix([[1] for _ in range(10000)]) == [[1] for _ in range(10000)]

def test_sort_matrix_non_numeric_input():
    with pytest.raises(TypeError):
        sort_matrix([[1, 'a'], [3, 4]])

def test_sort_matrix_mixed_numeric_non_numeric_input():
    with pytest.raises(TypeError):
        sort_matrix([[1, 'a'], [3, 4], [5, 'b']])

