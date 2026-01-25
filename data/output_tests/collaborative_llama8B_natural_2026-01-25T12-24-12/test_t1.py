import pytest
from data.input_code.t1 import *

@pytest.mark.parametrize('cost, m, n, expected', [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2, 15)
])
def test_min_cost_success(cost, m, n, expected):
    assert min_cost(cost, m, n) == expected

def test_min_cost_empty_matrix():
    with pytest.raises(IndexError):
        min_cost([], 2, 2)







def test_min_cost_m_equals_n():
    assert min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2) == 15


