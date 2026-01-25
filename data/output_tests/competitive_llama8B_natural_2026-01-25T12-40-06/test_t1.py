import pytest
from data.input_code.t1 import *

@pytest.mark.parametrize('cost, m, n, expected', [
    ([[1,2,3], [4,5,6], [7,8,9]], 2, 2, 15),
    ([[0,0,0], [0,0,0], [0,0,0]], 2, 2, 0),
])
def test_min_cost_success(cost, m, n, expected):
    assert min_cost(cost, m, n) == expected



def test_min_cost_matrix_with_zeros():
    assert min_cost([[1,0,3], [0,5,6], [7,8,9]], 2, 2) == 15

def test_min_cost_increasing_values():
    assert min_cost([[1,2,3], [4,5,6], [7,8,9]], 2, 2) == 15

def test_min_cost_decreasing_values():
    assert min_cost([[9,8,7], [6,5,4], [3,2,1]], 2, 2) == 15



