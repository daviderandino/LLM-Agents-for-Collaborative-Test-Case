import pytest
from data.input_code.t12 import *


def test_sort_matrix_error_non_matrix_input():
    M = "not a matrix"
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_error_non_list_input():
    M = 123
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_error_empty_input():
    M = []
    assert sort_matrix(M) == []

def test_sort_matrix_error_single_element_input():
    M = [1, 2, 3]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_error_non_2d_input_single_row():
    M = [1, 2, 3]
    with pytest.raises(TypeError):
        sort_matrix(M)

