import pytest
from data.input_code.t3 import is_not_prime

def test_is_not_prime_success():
    assert is_not_prime(36) == True

def test_is_not_prime_failure():
    assert is_not_prime(37) == False

def test_is_not_prime_zero():
    assert is_not_prime(0) == False


def test_is_not_prime_one():
    assert is_not_prime(1) == False

def test_is_not_prime_prime():
    assert is_not_prime(2) == False

def test_is_not_prime_empty_input():
    with pytest.raises(TypeError):
        is_not_prime(None)


def test_is_not_prime_min_input():
    assert is_not_prime(1) == False

