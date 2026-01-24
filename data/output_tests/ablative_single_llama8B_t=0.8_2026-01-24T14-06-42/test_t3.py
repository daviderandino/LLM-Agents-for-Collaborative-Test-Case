import pytest
from data.input_code.t3 import is_not_prime


def test_is_not_prime_none():
    with pytest.raises(TypeError):
        is_not_prime(None)

def test_is_not_prime_empty_list():
    with pytest.raises(TypeError):
        is_not_prime([])

def test_is_not_prime_empty_string():
    with pytest.raises(TypeError):
        is_not_prime("")