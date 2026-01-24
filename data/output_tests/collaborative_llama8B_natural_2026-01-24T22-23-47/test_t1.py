import pytest
from data.input_code.t1 import *


def test_min_cost_invalid_input_m():
    with pytest.raises(IndexError):
        min_cost([[[1, 2], [3, 4]]], 0, 2)

def test_min_cost_invalid_input_n():
    with pytest.raises(IndexError):
        min_cost([[[1, 2], [3, 4]]], 2, 0)






def test_min_cost_invalid_input_cost():
    with pytest.raises(IndexError):
        min_cost([[[1, 2], [3, 4]]], 3, 3)

def test_min_cost_invalid_input_m_and_n():
    with pytest.raises(IndexError):
        min_cost([[[1, 2], [3, 4]]], 2, 2)