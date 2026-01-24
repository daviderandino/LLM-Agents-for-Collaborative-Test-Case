import pytest
from data.input_code.t20 import multiples_of_num

def test_multiples_of_num_zero():
    assert multiples_of_num(0, 1) == []




def test_multiples_of_num_n_none():
    with pytest.raises(TypeError):
        multiples_of_num(2, None)

def test_multiples_of_num_m_none():
    with pytest.raises(TypeError):
        multiples_of_num(None, 2)

def test_multiples_of_num_both_none():
    with pytest.raises(TypeError):
        multiples_of_num(None, None)