import pytest
from data.input_code.t1 import *





def test_min_cost_0x0_matrix():
    cost = [[0]]
    m, n = 0, 0
    assert min_cost(cost, m, n) == 0





