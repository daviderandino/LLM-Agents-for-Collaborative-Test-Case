import pytest
from data.input_code.t1 import min_cost






def test_min_cost_none():
    cost = None
    m = 2
    n = 2
    with pytest.raises(TypeError):
        min_cost(cost, m, n)



