import pytest
from data.input_code.t3 import *



def test_is_not_prime_non_integer():
    with pytest.raises(TypeError):
        is_not_prime('a')

def test_is_not_prime_complex():
    with pytest.raises(TypeError):
        is_not_prime(3+4j)

def test_is_not_prime_negative():
    with pytest.raises(ValueError):
        is_not_prime(-5)  # Added test for negative number