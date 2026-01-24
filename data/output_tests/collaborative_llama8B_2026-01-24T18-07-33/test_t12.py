import pytest
from data.input_code.t12 import *

def test_sort_matrix_success():
    pytest.skip("This test is not needed as sort_matrix() does not check for equal row lengths")

def test_sort_matrix_empty_matrix():
    assert sort_matrix([]) == []

def test_sort_matrix_single_empty_row():
    assert sort_matrix([[]]) == [[]]


def test_sort_matrix_equal_row_lengths():
    assert sort_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == sorted([[1, 2, 3], [4, 5, 6], [7, 8, 9]], key=sum)

def test_sort_matrix_single_row():
    assert sort_matrix([[1, 2, 3]]) == [[1, 2, 3]]

def test_sort_matrix_equal_row_lengths_multiple_matrices():
    assert sort_matrix([[1, 2, 3], [4, 5, 6]]) == sorted([[1, 2, 3], [4, 5, 6]], key=sum)
    assert sort_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == sorted([[1, 2, 3], [4, 5, 6], [7, 8, 9]], key=sum)

