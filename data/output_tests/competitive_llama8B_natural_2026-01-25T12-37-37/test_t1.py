import pytest
from data.input_code.t1 import *





def test_min_cost_zero():
    cost = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    m, n = 2, 2
    assert min_cost(cost, m, n) == 0





