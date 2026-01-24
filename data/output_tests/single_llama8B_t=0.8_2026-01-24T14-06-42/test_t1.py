import pytest
from data.input_code.t1 import min_cost





def test_min_cost_invalid_cost():
    cost = [[1, 2, 3],
            [1, 2, 3],
            [1, 2]]
    m, n = 2, 3
    with pytest.raises(IndexError):
        min_cost(cost, m, n)


def test_min_cost_zero_cost():
    cost = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    m, n = 2, 2
    assert min_cost(cost, m, n) == 0