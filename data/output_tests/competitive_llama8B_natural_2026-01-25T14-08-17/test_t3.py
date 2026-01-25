import pytest
from data.input_code.t3 import *


def test_is_not_prime_error():
    with pytest.raises(TypeError):
        is_not_prime(None)

@pytest.mark.parametrize('n, expected', [
    (2, False),
    (3, False),
    (1000003, False),
])
def test_is_not_prime_edge_cases(n, expected):
    assert is_not_prime(n) == expected


def test_is_not_prime_success_zero():
    assert is_not_prime(0) == False

def test_is_not_prime_success_one():
    assert is_not_prime(1) == False