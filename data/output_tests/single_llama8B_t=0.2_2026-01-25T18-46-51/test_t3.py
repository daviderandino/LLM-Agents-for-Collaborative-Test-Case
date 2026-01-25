import pytest
from data.input_code.t3 import is_not_prime

def test_is_not_prime_success():
    assert is_not_prime(4) == True
    assert is_not_prime(6) == True
    assert is_not_prime(8) == True

def test_is_not_prime_prime_numbers():
    assert is_not_prime(2) == False
    assert is_not_prime(3) == False
    assert is_not_prime(5) == False

def test_is_not_prime_edge_cases():
    assert is_not_prime(0) == False
    assert is_not_prime(1) == False



def test_is_not_prime_non_numeric():
    with pytest.raises(TypeError):
        is_not_prime("hello")

def test_is_not_prime_empty_list():
    with pytest.raises(TypeError):
        is_not_prime([])

def test_is_not_prime_none():
    with pytest.raises(TypeError):
        is_not_prime(None)