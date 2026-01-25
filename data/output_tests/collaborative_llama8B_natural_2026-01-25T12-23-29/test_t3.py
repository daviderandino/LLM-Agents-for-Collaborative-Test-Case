import pytest
from data.input_code.t3 import *


def test_is_not_prime_zero_boundary():
    assert is_not_prime(0) == False

def test_is_not_prime_one_boundary():
    assert is_not_prime(1) == False


def test_is_not_prime_prime_boundary():
    assert is_not_prime(2) == False

def test_is_not_prime_large_number():
    assert is_not_prime(1000000) == True

