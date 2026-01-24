import pytest
from data.input_code.t3 import is_not_prime
import math

def test_is_not_prime_success():
    """Test is_not_prime function with a non-prime number."""
    assert is_not_prime(4) == True




def test_is_not_prime_edge_case_prime_number():
    """Test is_not_prime function with a prime number."""
    assert is_not_prime(5) == False

def test_is_not_prime_edge_case_prime_number_square():
    """Test is_not_prime function with a prime number squared."""
    assert is_not_prime(25) == True

def test_is_not_prime_invalid_input_type():
    """Test is_not_prime function with non-integer input."""
    with pytest.raises(TypeError):
        is_not_prime("a")

def test_is_not_prime_invalid_input_type_list():
    """Test is_not_prime function with non-integer input (list)."""
    with pytest.raises(TypeError):
        is_not_prime([1, 2, 3])

def test_is_not_prime_empty_string():
    """Test is_not_prime function with empty string input."""
    with pytest.raises(TypeError):
        is_not_prime("")

def test_is_not_prime_none_input():
    """Test is_not_prime function with None input."""
    with pytest.raises(TypeError):
        is_not_prime(None)