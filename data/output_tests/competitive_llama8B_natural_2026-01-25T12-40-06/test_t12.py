import pytest
from data.input_code.t12 import *


def test_sort_matrix_empty():
    assert sort_matrix([]) == []

def test_sort_matrix_string():
    with pytest.raises(TypeError):
        sort_matrix([[1, 2, 3], ['a', 'b', 'c'], [4, 5, 6]])

def test_sort_matrix_non_numeric():
    with pytest.raises(TypeError):
        sort_matrix([[1, 2, 3], [4, 'a', 6], [7, 8, 9]])