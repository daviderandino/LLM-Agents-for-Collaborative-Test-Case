import pytest
from data.input_code.t3 import is_not_prime

def test_is_not_prime_success():
    assert is_not_prime(4) == True
    assert is_not_prime(9) == True
    assert is_not_prime(6) == True

def test_is_not_prime_prime():
    assert is_not_prime(2) == False
    assert is_not_prime(7) == False
    assert is_not_prime(3) == False

def test_is_not_prime_zero():
    assert is_not_prime(0) == False  # Based on the given code, 0 is not considered a prime number


def test_is_not_prime_one():
    assert is_not_prime(1) == False  # Based on the given code, 1 is not considered a prime number

def test_is_not_prime_empty():
    with pytest.raises(TypeError):
        is_not_prime(None)

def test_is_not_prime_string():
    with pytest.raises(TypeError):
        is_not_prime("hello")

def test_is_not_prime_list():
    with pytest.raises(TypeError):
        is_not_prime([])