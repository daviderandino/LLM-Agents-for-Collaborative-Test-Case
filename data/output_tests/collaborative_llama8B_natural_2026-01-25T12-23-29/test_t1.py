import pytest
from matrix_chain_multiplication import *

@pytest.mark.parametrize('R, C, cost, expected', [
    (2, 2, [[1, 2], [3, 4]], 7),
    (3, 3, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 9),
])
def test_min_cost_success(R, C, cost, expected):
    assert min_cost(cost, R, C) == expected

@pytest.mark.parametrize('R, C, cost, expected', [
    (2, 2, [[1, 0], [3, 4]], 4),
])
def test_min_cost_zero_value(R, C, cost, expected):
    assert min_cost(cost, R, C) == expected

@pytest.mark.parametrize('R, C, cost, expected', [
    (3, 3, [[1, -2, 3], [-3, 1, 2], [2, -1, 3]], 5),
])
def test_min_cost_negative_values(R, C, cost, expected):
    assert min_cost(cost, R, C) == expected

@pytest.mark.parametrize('R, C, cost, expected', [
    (1, 1, [[5]], 5),
])
def test_min_cost_single_matrix(R, C, cost, expected):
    assert min_cost(cost, R, C) == expected

@pytest.mark.parametrize('R, C, cost, expected', [
    (2, 2, [[1]*9 for _ in range(2)], 14),
])
def test_min_cost_large_cost_matrix(R, C, cost, expected):
    assert min_cost(cost, R, C) == expected

@pytest.mark.parametrize('R, C, cost, expected', [
    (3, 3, [[0, 1, 1], [1, 1, 1], [1, 1, 1]], 3),
])
def test_min_cost_zero_row(R, C, cost, expected):
    assert min_cost(cost, R, C) == expected

@pytest.mark.parametrize('R, C, cost, expected', [
    (2, 2, [[0, 0], [0, 0]], 0),
])
def test_min_cost_zero_cost(R, C, cost, expected):
    assert min_cost(cost, R, C) == expected

def test_min_cost_invalid_input():
    with pytest.raises(ValueError):
        min_cost([[1, 2], [3, 4]], 2, 0)

def test_min_cost_invalid_cost_matrix():
    with pytest.raises(ValueError):
        min_cost([[1, 2], [3, 4]], 2, 2)