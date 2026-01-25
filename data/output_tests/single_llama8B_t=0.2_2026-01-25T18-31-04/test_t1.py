import pytest
from data.input_code.t1 import min_cost


def test_min_cost_empty_cost():
    cost = []
    m = 2
    n = 2
    with pytest.raises(IndexError):
        min_cost(cost, m, n)


def test_min_cost_empty_n():
    cost = [[1, 2, 3]]
    m = 2
    n = 0
    with pytest.raises(IndexError):
        min_cost(cost, m, n)


def test_min_cost_negative_n():
    cost = [[1, 2, 3]]
    m = 2
    n = -1
    with pytest.raises(IndexError):
        min_cost(cost, m, n)

def test_min_cost_non_integer_m():
    cost = [[1, 2, 3], [4, 5, 6]]
    m = 2.5
    n = 2
    with pytest.raises(TypeError):
        min_cost(cost, m, n)

