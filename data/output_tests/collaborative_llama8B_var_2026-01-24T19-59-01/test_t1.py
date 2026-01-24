import pytest
from data.input_code.t1 import *


def test_min_cost_zero_row():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2)

def test_min_cost_zero_column():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3)


def test_min_cost_zero_n():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6]], 2, 0)

def test_min_cost_success_zero_cost():
    assert min_cost([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 2, 2) == 0

def test_min_cost_success_zero_m_zero_n():
    assert min_cost([[0, 0], [0, 0]], 0, 0) == 0







def test_min_cost_success_n_zero():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6]], 2, 0)