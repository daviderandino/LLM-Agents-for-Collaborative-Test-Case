import pytest
from data.input_code.t20 import *

def test_multiples_of_num_positive_numbers():
    assert multiples_of_num(3, 2) == [2, 4, 6]


def test_multiples_of_num_negative_numbers():
    assert multiples_of_num(-3, 2) == []


def test_multiples_of_num_zero_n():
    with pytest.raises(ValueError):
        multiples_of_num(3, 0)

def test_multiples_of_num_large_numbers():
    assert multiples_of_num(1000, 2) == list(range(2, 2001, 2))


def test_multiples_of_num_non_integer_m():
    with pytest.raises(TypeError):
        multiples_of_num(3.5, 2)

def test_multiples_of_num_non_integer_n():
    with pytest.raises(TypeError):
        multiples_of_num(3, 2.5)