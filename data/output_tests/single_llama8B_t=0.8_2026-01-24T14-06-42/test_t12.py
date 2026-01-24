import pytest
from data.input_code.t12 import sort_matrix

def test_sort_matrix_default():
    matrix1 = [[1, 2], [3, 4], [5, 6]]
    expected_result = [[1, 2], [3, 4], [5, 6]]
    result = sort_matrix(matrix1)
    assert result == expected_result

def test_sort_matrix_empty_matrix():
    matrix = []
    expected_result = []
    result = sort_matrix(matrix)
    assert result == expected_result

def test_sort_matrix_single_element_matrix():
    matrix = [[1]]
    expected_result = [[1]]
    result = sort_matrix(matrix)
    assert result == expected_result

def test_sort_matrix_matrix_with_negative_numbers():
    matrix = [[-3, -2], [-1, 0], [1, 2]]
    expected_result = [[-3, -2], [-1, 0], [1, 2]]
    result = sort_matrix(matrix)
    assert result == expected_result

def test_sort_matrix_matrix_with_zero():
    matrix = [[0, 1], [1, 0], [2, 2]]
    expected_result = [[0, 1], [1, 0], [2, 2]]
    result = sort_matrix(matrix)
    assert result == expected_result

def test_sort_matrix_matrix_with_float_numbers():
    matrix = [[1.5, 2.5], [3.5, 4.5], [5.5, 6.5]]
    expected_result = [[1.5, 2.5], [3.5, 4.5], [5.5, 6.5]]
    result = sort_matrix(matrix)
    assert result == expected_result

def test_sort_matrix_matrix_with_non_numeric_elements():
    matrix = [[1, 'a'], [3, 4], [5, 'b']]
    with pytest.raises(TypeError):
        sort_matrix(matrix)

def test_sort_matrix_matrix_with_large_elements():
    matrix = [[100000, 200000], [300000, 400000], [500000, 600000]]
    expected_result = [[100000, 200000], [300000, 400000], [500000, 600000]]
    result = sort_matrix(matrix)
    assert result == expected_result


def test_sort_matrix_matrix_with_single_row():
    matrix = [[1, 2, 3, 4, 5]]
    expected_result = [[1, 2, 3, 4, 5]]
    result = sort_matrix(matrix)
    assert result == expected_result

def test_sort_matrix_matrix_with_single_col():
    matrix = [[1], [2], [3], [4], [5]]
    expected_result = [[1], [2], [3], [4], [5]]
    result = sort_matrix(matrix)
    assert result == expected_result