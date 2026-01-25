import pytest
from data.input_code.t12 import *

def test_sort_matrix_sorted():
    assert sort_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def test_sort_matrix_sorted_descending():
    assert sort_matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]]) == [[3, 2, 1], [6, 5, 4], [9, 8, 7]]

def test_sort_matrix_empty():
    assert sort_matrix([]) == []

def test_sort_matrix_non_list():
    with pytest.raises(TypeError):
        sort_matrix("not a matrix")