import pytest
from data.input_code.t20 import *



def test_multiples_of_num_zero_multiplicand():
    with pytest.raises(ValueError):
        multiples_of_num(3, 0)



def test_multiples_of_num_string_input():
    with pytest.raises(TypeError):
        multiples_of_num(3, '2')

def test_multiples_of_num_non_integer_input():
    with pytest.raises(TypeError):
        multiples_of_num(3.5, 2.5)

