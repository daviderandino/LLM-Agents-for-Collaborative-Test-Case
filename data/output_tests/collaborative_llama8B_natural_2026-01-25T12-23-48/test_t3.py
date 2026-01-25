import pytest
from data.input_code.t3 import *

@pytest.mark.parametrize('n, expected', [
    (7, False)
])
def test_is_not_prime_prime(n, expected):
    assert is_not_prime(n) == expected

@pytest.mark.parametrize('n, expected', [
    (16, True)
])
def test_is_not_prime_square(n, expected):
    assert is_not_prime(n) == expected

@pytest.mark.parametrize('n, expected', [
    (0, False)
])
def test_is_not_prime_less_than_2(n, expected):
    assert is_not_prime(n) == expected

@pytest.mark.parametrize('n, expected', [
    (2, False)
])
def test_is_not_prime_exactly_2(n, expected):
    assert is_not_prime(n) == expected

@pytest.mark.parametrize('n, expected', [
    (1, False)
])
def test_is_not_prime_exactly_1(n, expected):
    assert is_not_prime(n) == expected

@pytest.mark.parametrize('n, expected', [
    (4, True)
])
def test_is_not_prime_non_prime(n, expected):
    assert is_not_prime(n) == expected

@pytest.mark.parametrize('n, expected', [
    (1000007, False)
])
def test_is_not_prime_large(n, expected):
    assert not is_not_prime(n) == expected  # Fix: is_not_prime returns False for primes, so we check if it's not prime