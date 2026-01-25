import pytest
from data.input_code.t3 import *

def test_is_not_prime_prime():
    assert not is_not_prime(7)

def test_is_not_prime_composite():
    assert is_not_prime(10)

def test_is_not_prime_zero():
    assert not is_not_prime(0)

def test_is_not_prime_one():
    assert not is_not_prime(1)

def test_is_not_prime_negative():
    with pytest.raises(ValueError):
        is_not_prime(-5)

def test_is_not_prime_negative_one():
    with pytest.raises(ValueError):
        is_not_prime(-1)

def test_is_not_prime_negative_composite():
    with pytest.raises(ValueError):  # is_not_prime() raises ValueError for negative numbers
        is_not_prime(-2)


def test_is_not_prime_non_numeric():
    with pytest.raises(TypeError):
        is_not_prime(None)