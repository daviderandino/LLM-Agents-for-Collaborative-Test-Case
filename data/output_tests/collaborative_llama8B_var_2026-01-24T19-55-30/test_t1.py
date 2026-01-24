import pytest
from data.input_code.t1 import *


def test_min_cost_zero_rows():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0, 3)

def test_min_cost_zero_cols():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 0)



def test_min_cost_success_cost_1_2_3_4_5():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)