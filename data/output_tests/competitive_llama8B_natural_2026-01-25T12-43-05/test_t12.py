import pytest
from data.input_code.t12 import *

def test_sort_matrix_happy_path_2x2():
    M = [[1,2],[3,4]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_happy_path_3x3():
    M = [[1,2,3],[4,5,6],[7,8,9]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_duplicate_row_sums():
    M = [[1,2,3],[4,5,6],[1,2,3]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_empty_matrix():
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_single_row():
    M = [[1,2,3]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_single_column():
    M = [[1],[2],[3]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_non_numeric_values():
    M = [[1,'a',3],[4,5,6],[7,8,9]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_non_list_values():
    M = [1,'a',3]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_mixed_numeric_non_numeric_values():
    M = [[1,'a',3],[4,'b',6],[7,8,9]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_non_numeric_values_in_sum_calculation():
    M = [[1,'a',3],[4,'abc',6],[7,8,9]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_happy_path_2x2_corrected():
    M = [[1,2],[3,4]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_happy_path_3x3_corrected():
    M = [[1,2,3],[4,5,6],[7,8,9]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_duplicate_row_sums_corrected():
    M = [[1,2,3],[4,5,6],[1,2,3]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_empty_matrix_corrected():
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_single_row_corrected():
    M = [[1,2,3]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected

def test_sort_matrix_single_column_corrected():
    M = [[1],[2],[3]]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected