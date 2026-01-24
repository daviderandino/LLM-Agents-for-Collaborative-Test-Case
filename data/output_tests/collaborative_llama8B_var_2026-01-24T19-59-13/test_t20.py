import pytest
from data.input_code.t20 import *


def test_multiples_of_num_edge_m_zero():
    assert multiples_of_num(0, 2) == []

def test_multiples_of_num_edge_n_zero():
    with pytest.raises(ValueError):
        multiples_of_num(5, 0)

def test_multiples_of_num_edge_m_n_zero():
    with pytest.raises(ValueError):
        multiples_of_num(0, 0)


