import pytest
from data.input_code.t12 import *



def test_sort_matrix_non_list_input():
    with pytest.raises(TypeError):
        sort_matrix([1, 2, 3, 4])

def test_sort_matrix_non_numeric_values():
    with pytest.raises(TypeError):
        sort_matrix([[1, 'a'], [2, 3]])

def test_sort_matrix_non_list_rows():
    with pytest.raises(TypeError):
        sort_matrix([[1, 2], [3, 4], 5])

def test_sort_matrix_empty_matrix():
    assert sort_matrix([]) == []

def test_sort_matrix_single_row_matrix():
    assert sort_matrix([[1, 2]]) == [[1, 2]]

def test_sort_matrix_single_column_matrix():
    assert sort_matrix([[1], [2]]) == [[1], [2]]

def test_sort_matrix_invalid_input():
    with pytest.raises(TypeError):
        sort_matrix([[1, 2], [3, 'a']])  # Added a non-numeric value to the second list

