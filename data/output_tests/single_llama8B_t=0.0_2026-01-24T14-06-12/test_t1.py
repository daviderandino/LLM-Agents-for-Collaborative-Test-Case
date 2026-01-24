import pytest
from data.input_code.t1 import min_cost


def test_min_cost_empty_cost():
    cost = []
    m = 0
    n = 0
    with pytest.raises(IndexError):
        min_cost(cost, m, n)

def test_min_cost_empty_cost_with_dimensions():
    cost = []
    m = 2
    n = 2
    with pytest.raises(IndexError):
        min_cost(cost, m, n)

def test_min_cost_invalid_dimensions():
    cost = [[1, 2, 3], [4, 5, 6]]
    m = 2
    n = 3
    with pytest.raises(IndexError):
        min_cost(cost, m, n)

def test_min_cost_zero_cost():
    cost = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    m = 2
    n = 2
    expected = 0
    assert min_cost(cost, m, n) == expected


