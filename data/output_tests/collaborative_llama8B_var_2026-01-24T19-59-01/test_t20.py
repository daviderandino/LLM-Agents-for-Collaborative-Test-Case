import pytest
from data.input_code.t20 import *

@pytest.mark.parametrize('m, n, expected', [
    (5, 2, [2, 4, 6, 8, 10]),
    (5, 1, [1, 2, 3, 4, 5]),
    (5, -2, [-2, -4, -6, -8, -10])
])
def test_multiples_of_num_success(m, n, expected):
    assert multiples_of_num(m, n) == expected


def test_multiples_of_num_zero_m():
    assert multiples_of_num(0, 2) == []

