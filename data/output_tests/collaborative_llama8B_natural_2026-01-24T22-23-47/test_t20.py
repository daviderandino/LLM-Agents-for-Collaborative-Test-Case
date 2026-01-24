import pytest
from data.input_code.t20 import *


def test_multiples_of_num_zero_multiplier():
    assert multiples_of_num(0, 2) == []




def test_multiples_of_num_non_integer_multiplier():
    with pytest.raises(TypeError):
        multiples_of_num(5.5, 2)

def test_multiples_of_num_non_integer_number():
    with pytest.raises(TypeError):
        multiples_of_num(5, 2.5)