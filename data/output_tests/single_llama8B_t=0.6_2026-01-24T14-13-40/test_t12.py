import pytest

from data.input_code.t12 import sort_matrix


def test_sort_matrix_empty():
    # Test with an empty matrix
    M = []
    expected = []
    assert sort_matrix(M) == expected

def test_sort_matrix_single_row():
    # Test with a matrix containing a single row
    M = [[1, 2, 3]]
    expected = [[1, 2, 3]]
    assert sort_matrix(M) == expected

def test_sort_matrix_single_element():
    # Test with a matrix containing a single element
    M = [[5]]
    expected = [[5]]
    assert sort_matrix(M) == expected

def test_sort_matrix_none():
    # Test with a None input
    with pytest.raises(TypeError):
        sort_matrix(None)

def test_sort_matrix_non_numeric():
    # Test with a matrix containing non-numeric values
    M = [[1, 'a'], [2, 4]]
    with pytest.raises(TypeError):
        sort_matrix(M)

def test_sort_matrix_large_matrix():
    # Test with a large matrix
    import random
    M = [[random.randint(0, 100) for _ in range(10)] for _ in range(10)]
    expected = sorted(M, key=sum)
    assert sort_matrix(M) == expected