import pytest
from data.input_code.t3 import *

def test_is_not_prime_false():
    assert is_not_prime(5) == False

def test_is_not_prime_true():
    assert is_not_prime(8) == True

def test_is_not_prime_min():
    assert is_not_prime(2) == False

def test_is_not_prime_max():
    assert is_not_prime(100) == True


def test_is_not_prime_negative():
    with pytest.raises(ValueError):
        is_not_prime(-5)

def test_is_not_prime_zero_result():
    assert is_not_prime(0) == False

