import pytest
from data.input_code.t3 import *
import math


def test_is_not_prime_large_number():
    assert is_not_prime(1000003) == False



def test_is_not_prime_empty_input():
    with pytest.raises(TypeError):
        is_not_prime(None)

