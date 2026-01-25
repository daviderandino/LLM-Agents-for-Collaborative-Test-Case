import pytest
from data.input_code.t1 import min_cost






def test_min_cost_zero_cost():
    cost = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    m = 2
    n = 2
    expected = 0
    assert min_cost(cost, m, n) == expected

def test_min_cost_none_cost():
    cost = None
    m = 2
    n = 2
    with pytest.raises(TypeError):
        min_cost(cost, m, n)

def test_min_cost_empty_cost_list():
    cost = []
    m = 2
    n = 2
    with pytest.raises(IndexError):
        min_cost(cost, m, n)

