import pytest
from data.input_code.t20 import *

@pytest.mark.parametrize('m, n, expected', [
    (10, 2, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
])
def test_multiples_of_num_positive(m, n, expected):
    assert multiples_of_num(m, n) == expected

def test_multiples_of_num_zero_multiplier():
    with pytest.raises(ValueError):
        multiples_of_num(5, 0)

def test_multiples_of_num_negative_multiplier():
    assert multiples_of_num(-5, 2) == []


def test_multiples_of_num_positive_number_zero_multiplier():
    with pytest.raises(ValueError):
        multiples_of_num(5, 0)

def test_multiples_of_num_large_positive_numbers():
    assert multiples_of_num(100, 10) == list(range(10, 1001, 10))

def test_multiples_of_num_negative_numbers():
    assert multiples_of_num(-5, -2) == []



