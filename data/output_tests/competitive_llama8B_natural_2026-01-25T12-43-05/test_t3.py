import pytest
from data.input_code.t3 import *
import math

def test_is_not_prime_prime_number():
    assert is_not_prime(7) == False

def test_is_not_prime_composite_number():
    assert is_not_prime(4) == True

def test_is_not_prime_boundary_condition_1():
    assert is_not_prime(1) == False


def test_is_not_prime_negative_number():
    with pytest.raises(ValueError):
        is_not_prime(-5)


def test_is_not_prime_non_numeric_input():
    with pytest.raises(TypeError):
        is_not_prime('5')

def test_is_not_prime_large_number():
    assert is_not_prime(1000000) == True

def test_is_not_prime_special_case_2():
    assert is_not_prime(2) == False

def test_is_not_prime_special_case_3():
    assert is_not_prime(3) == False