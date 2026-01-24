import pytest
from data.input_code.t20 import multiples_of_num




def test_multiples_of_num_zero_multiple():
    assert multiples_of_num(0, 10) == []


def test_multiples_of_num_invalid_input():
    with pytest.raises(TypeError):
        multiples_of_num('a', 10)

def test_multiples_of_num_invalid_input2():
    with pytest.raises(TypeError):
        multiples_of_num(2, 'a')