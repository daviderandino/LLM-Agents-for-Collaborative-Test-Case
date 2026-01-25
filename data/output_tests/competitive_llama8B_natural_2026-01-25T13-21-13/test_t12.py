import pytest
from data.input_code.t12 import *



def test_sort_matrix_none():
    with pytest.raises(TypeError):
        sort_matrix(None)

def test_sort_matrix_non_list():
    with pytest.raises(TypeError):
        sort_matrix(5)

def test_sort_matrix_non_numeric():
    with pytest.raises(TypeError):
        sort_matrix([[1, 2, 'a'], [3, 4, 5]])