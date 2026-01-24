import pytest
from data.input_code.t3 import *

def test_is_not_prime_prime_number():
    assert not is_not_prime(11)

def test_is_not_prime_non_prime_number():
    assert is_not_prime(10)

def test_is_not_prime_number_less_than_2():
    assert not is_not_prime(1)


def test_is_not_prime_negative_number():
    with pytest.raises(ValueError):
        is_not_prime(-10)

def test_is_not_prime_number_equal_to_2():
    assert not is_not_prime(2)



def test_is_not_prime_large_prime_number():
    assert not is_not_prime(1000003)

def test_is_not_prime_large_non_prime_number():
    assert is_not_prime(1000004)