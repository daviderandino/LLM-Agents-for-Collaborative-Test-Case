import pytest
from data.input_code.t20 import *


def test_multiples_of_num_zero_multiplier():
    with pytest.raises(ValueError):
        multiples_of_num(5, 0)


def test_multiples_of_num_negative_multiplier():
    assert multiples_of_num(-10, 2) == []



def test_multiples_of_num_zero():
    with pytest.raises(ValueError):
        multiples_of_num(0, 0)

def test_multiples_of_num_large_numbers():
    assert multiples_of_num(1000, 5) == list(range(5, 5001, 5))

def test_multiples_of_num_empty_list():
    with pytest.raises(TypeError):
        multiples_of_num(None, 2)

def test_multiples_of_num_invalid_data_type():
    with pytest.raises(TypeError):
        multiples_of_num('a', 2)