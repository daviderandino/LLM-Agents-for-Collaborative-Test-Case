import pytest
from data.input_code.t20 import *

@pytest.mark.parametrize('m, n, expected', [
    (5, 3, [3, 6, 9, 12, 15])
])
def test_multiples_of_num_happy_path(m, n, expected):
    assert multiples_of_num(m, n) == expected


def test_multiples_of_num_zero_input():
    assert multiples_of_num(0, 3) == []


def test_multiples_of_num_both_negative_input():
    assert multiples_of_num(-5, -3) == []

def test_multiples_of_num_large_input():
    assert multiples_of_num(1000, 3) == list(range(3, 3003, 3))


def test_multiples_of_num_non_integer_input():
    with pytest.raises(TypeError):
        multiples_of_num(5.5, 3)