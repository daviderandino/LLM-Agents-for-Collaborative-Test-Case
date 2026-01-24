import pytest
from data.input_code.t1 import min_cost





def test_min_cost_empty_cost_list():
    cost = []
    m = 1
    n = 1
    with pytest.raises(IndexError):
        min_cost(cost, m, n)




