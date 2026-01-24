import pytest

from data.input_code.t20 import multiples_of_num

def test_multiples_of_num_valid_positive_input():
    assert multiples_of_num(2, 10) == [10, 20]



def test_multiples_of_num_zero_multiple_of_zero():
    assert multiples_of_num(0, 5) == []





