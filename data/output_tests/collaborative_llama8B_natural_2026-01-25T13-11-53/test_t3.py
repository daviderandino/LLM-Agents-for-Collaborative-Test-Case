import pytest
from data.input_code.t3 import *


def test_is_not_prime_zero_error():
    with pytest.raises(TypeError):
        is_not_prime('a')


def test_is_not_prime_negative_input():
    with pytest.raises(ValueError):
        is_not_prime(-5)

