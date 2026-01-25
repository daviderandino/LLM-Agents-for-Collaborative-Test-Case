import pytest
from data.input_code.t1 import *

@pytest.mark.parametrize('cost, m, n, expected', [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2, 15)
])
def test_min_cost_success(cost, m, n, expected):
    assert min_cost(cost, m, n) == expected

def test_min_cost_zero_cost():
    assert min_cost([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 2, 2) == 0

def test_min_cost_out_of_bounds_m():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2)

def test_min_cost_out_of_bounds_n():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3)



def test_min_cost_negative_cost():
    assert min_cost([[1, 2, 3], [4, -5, 6], [7, 8, 9]], 2, 2) == 5

def test_min_cost_floating_point_cost():
    assert min_cost([[1.5, 2.5, 3.5], [4.5, 5.5, 6.5], [7.5, 8.5, 9.5]], 2, 2) == 16.5