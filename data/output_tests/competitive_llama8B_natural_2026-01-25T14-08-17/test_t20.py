import pytest
from data.input_code.t20 import *


def test_multiples_of_num_zero_multiplier():
    assert multiples_of_num(0, 5) == []

def test_multiples_of_num_zero_multiple():
    with pytest.raises(ValueError):
        multiples_of_num(5, 0)



def test_multiples_of_num_both_negative():
    assert multiples_of_num(-5, -2) == []

def test_multiples_of_num_non_integer_multiplier():
    with pytest.raises(TypeError):
        multiples_of_num(5.5, 2)

def test_multiples_of_num_non_integer_multiple():
    with pytest.raises(TypeError):
        multiples_of_num(5, 2.5)


def test_multiples_of_num_m_equal_to_n():
    assert multiples_of_num(5, 5) == [5, 10, 15, 20, 25]