import pytest
from data.input_code.t1 import min_cost


def test_min_cost_empty_cost():
    cost = []
    m = 0
    n = 0
    with pytest.raises(IndexError):
        min_cost(cost, m, n)

def test_min_cost_zero_rows():
    cost = [[1, 2, 3]]
    m = 0
    n = 3
    with pytest.raises(IndexError):
        min_cost(cost, m, n)

def test_min_cost_zero_cols():
    cost = [[1, 2, 3], [4, 5, 6]]
    m = 2
    n = 0
    with pytest.raises(IndexError):
        min_cost(cost, m, n)



def test_min_cost_non_integer_rows():
    cost = [[1, 2, 3], [4, 5, 6]]
    m = 2.5
    n = 3
    with pytest.raises(TypeError):
        min_cost(cost, m, n)

