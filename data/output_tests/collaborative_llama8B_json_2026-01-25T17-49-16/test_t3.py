import pytest
from data.input_code.t3 import *


def test_is_not_prime_error():
    with pytest.raises(TypeError):
        is_not_prime("a")

def test_is_not_prime_negative():
    with pytest.raises(ValueError):
        is_not_prime(-5)


def test_is_not_prime_none():
    with pytest.raises(TypeError):
        is_not_prime(None)


def test_is_not_prime_non_numeric():
    with pytest.raises(TypeError):
        is_not_prime("a")

def test_is_not_prime_non_numeric_type():
    with pytest.raises(TypeError):
        is_not_prime("a")


