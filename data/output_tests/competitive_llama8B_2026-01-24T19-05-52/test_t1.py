import pytest
from data.input_code.t1 import *


def test_min_cost_zero_row():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_zero_column():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 0)

def test_min_cost_zero_m():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0, 3)

def test_min_cost_zero_n():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 0)