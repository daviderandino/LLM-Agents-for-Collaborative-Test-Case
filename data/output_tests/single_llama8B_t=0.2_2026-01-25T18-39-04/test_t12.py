import pytest
from data.input_code.t12 import sort_matrix


def test_sort_matrix_empty_matrix():
    # Test case with an empty matrix
    M = []
    expected_result = []
    assert sort_matrix(M) == expected_result

def test_sort_matrix_single_row_matrix():
    # Test case with a single row matrix
    M = [[1, 2, 3]]
    expected_result = [[1, 2, 3]]
    assert sort_matrix(M) == expected_result

def test_sort_matrix_single_element_matrix():
    # Test case with a single element matrix
    M = [[1]]
    expected_result = [[1]]
    assert sort_matrix(M) == expected_result



def test_sort_matrix_large_matrix():
    # Test case with a large matrix
    import random
    M = [[random.randint(1, 100) for _ in range(10)] for _ in range(10)]
    expected_result = sorted(M, key=sum)
    assert sort_matrix(M) == expected_result