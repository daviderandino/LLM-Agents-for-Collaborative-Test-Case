import pytest
from data.input_code.t12 import *

def test_sort_matrix_2x2_happy_path():
    M = [[1,2],[3,4]]
    expected = [[1,2],[3,4]]
    assert sort_matrix(M) == expected

def test_sort_matrix_2x2_happy_path_2():
    M = [[4,3],[2,1]]
    expected = [[2,1],[4,3]]
    assert sort_matrix(M) == expected

def test_sort_matrix_2x2_happy_path_3():
    M = [[1,1],[1,1]]
    expected = [[1,1],[1,1]]
    assert sort_matrix(M) == expected


def test_sort_matrix_empty_matrix():
    M = []
    expected = []
    assert sort_matrix(M) == expected


def test_sort_matrix_non_numeric_values():
    M = [[1,'a',3],[4,5,6]]
    with pytest.raises(TypeError):
        sort_matrix(M)


def test_sort_matrix_float_values():
    M = [[1.5,2.5,3.5],[4.5,5.5,6.5]]
    expected = [[1.5,2.5,3.5],[4.5,5.5,6.5]]
    assert sort_matrix(M) == expected

def test_sort_matrix_large_values():
    M = [[1000000,2000000,3000000],[4000000,5000000,6000000]]
    expected = [[1000000,2000000,3000000],[4000000,5000000,6000000]]
    assert sort_matrix(M) == expected




def test_sort_matrix_float_values_2():
    M = [[1.5,2.5,3.5],[4.5,5.5,6.5]]
    expected = [[1.5,2.5,3.5],[4.5,5.5,6.5]]
    assert sort_matrix(M) == expected

def test_sort_matrix_large_values_2():
    M = [[1000000,2000000,3000000],[4000000,5000000,6000000]]
    expected = [[1000000,2000000,3000000],[4000000,5000000,6000000]]
    assert sort_matrix(M) == expected