import pytest
from data.input_code.t12 import *

def test_sort_matrix_happy_path_single_element():
    M = [[5]]
    assert sort_matrix(M) == [[5]]




def test_sort_matrix_exception_non_numeric_value():
    M = [[3, 'a'], [5, 1]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_happy_path_empty_matrix():
    M = []
    assert sort_matrix(M) == []

def test_sort_matrix_happy_path_single_row_of_zeros():
    M = [[0, 0]]
    assert sort_matrix(M) == [[0, 0]]

def test_sort_matrix_happy_path_single_column_of_zeros():
    M = [[0], [0]]
    assert sort_matrix(M) == [[0], [0]]




def test_sort_matrix_exception_non_list_element():
    M = [[3, 2], 5, [1]]
    with pytest.raises(TypeError):
        sort_matrix(M)