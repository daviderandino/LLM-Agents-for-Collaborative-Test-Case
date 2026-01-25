import pytest
from data.input_code.t12 import sort_matrix

def test_sort_matrix_empty_matrix():
    M = []
    assert sort_matrix(M) == []

def test_sort_matrix_single_element_matrix():
    M = [[1]]
    assert sort_matrix(M) == [[1]]

def test_sort_matrix_two_elements_matrix():
    M = [[1, 2], [3, 4]]
    assert sort_matrix(M) == [[1, 2], [3, 4]]


def test_sort_matrix_matrix_with_zero():
    M = [[0, 2], [3, 4]]
    assert sort_matrix(M) == [[0, 2], [3, 4]]

def test_sort_matrix_matrix_with_duplicates():
    M = [[1, 2], [1, 4]]
    assert sort_matrix(M) == [[1, 2], [1, 4]]

def test_sort_matrix_matrix_with_non_integer_elements():
    M = [[1.5, 2], [3, 4]]
    assert sort_matrix(M) == [[1.5, 2], [3, 4]]

def test_sort_matrix_matrix_with_non_list_elements():
    M = [[1, 2], [3, 'a']]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_matrix_with_non_numeric_elements():
    M = [[1, 'a'], [3, 4]]
    with pytest.raises(TypeError):
        sort_matrix(M)