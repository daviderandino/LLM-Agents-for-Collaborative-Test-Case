import pytest
from data.input_code.t1 import *





def test_min_cost_empty_matrices():
    cost = []
    with pytest.raises(IndexError):
        min_cost(cost, 3, 3)

def test_min_cost_invalid_input_m_zero_n_non_zero():
    cost = [[1], [2], [3]]
    with pytest.raises(IndexError):
        min_cost([], 0, 3)

def test_min_cost_invalid_input_n_zero_m_non_zero():
    cost = [[1, 2], [3, 4], [5, 6]]
    with pytest.raises(IndexError):
        min_cost([[1, 2], [3, 4], [5, 6]], 3, 0)




def test_min_cost_m_zero_n_non_zero():
    cost = [[1, 2, 3]]
    with pytest.raises(IndexError):
        min_cost(cost, 0, 3)

def test_min_cost_n_zero_m_non_zero():
    cost = [[1, 2], [3, 4], [5, 6]]
    with pytest.raises(IndexError):
        min_cost([[1, 2], [3, 4], [5, 6]], 3, 0)