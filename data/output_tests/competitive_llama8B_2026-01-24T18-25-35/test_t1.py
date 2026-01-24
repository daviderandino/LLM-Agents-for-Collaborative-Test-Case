import pytest
from data.input_code.t1 import *

def test_min_cost_valid_input():
    cost = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert min_cost(cost, 2, 2) == 15

def test_min_cost_invalid_dimensions():
    cost = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(IndexError):
        min_cost(cost, 3, 2)

def test_min_cost_invalid_dimensions_2():
    cost = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(IndexError):
        min_cost(cost, 2, 3)

def test_min_cost_zero_matrix():
    cost = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert min_cost(cost, 2, 2) == 0

def test_min_cost_non_square_matrix():
    cost = [[1], [2], [3]]
    with pytest.raises(IndexError):
        min_cost(cost, 2, 3)

def test_min_cost_mismatched_dimensions():
    cost = [[1, 2, 3], [4, 5, 6]]
    with pytest.raises(IndexError):
        min_cost(cost, 2, 3)