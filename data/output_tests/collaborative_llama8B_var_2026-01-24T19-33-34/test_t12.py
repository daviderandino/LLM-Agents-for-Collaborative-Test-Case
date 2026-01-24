import pytest
from data.input_code.t12 import *

def test_sort_matrix_success():
    M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert sort_matrix(M) == expected

def test_sort_matrix_success_descending():
    M = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    expected = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
    assert sort_matrix(M) == expected

def test_sort_matrix_error_non_list():
    M = [[1, 2, 3], [4, 5, 6], None]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_error_string():
    M = "string"
    with pytest.raises(TypeError):
        sort_matrix(M)


