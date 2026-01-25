import pytest
import math
from data.input_code.t3 import *

@pytest.mark.parametrize('n, expected', [
    (11, False),
    (12, True),
])
def test_is_not_prime_happy_path(n, expected):
    assert is_not_prime(n) == expected

@pytest.mark.parametrize('n, expected', [
    (0, False),
    (1, False),
    (2, False),
    (1000003, False),
])
def test_is_not_prime_boundary_conditions(n, expected):
    assert is_not_prime(n) == expected

def test_is_not_prime_large_input():
    assert is_not_prime(math.pow(10, 9)) == True  # Test large input handling


def test_is_not_prime_non_numeric_input():
    with pytest.raises(TypeError):
        is_not_prime('hello')


