import pytest

from data.input_code.t20 import multiples_of_num




def test_multiples_of_num_none_n():
    # Test none value for n
    with pytest.raises(TypeError):
        multiples_of_num(3, None)

def multiple_of_n(m, n, func):
    """Helper function to get multiples of n"""
    return func(m, n)

def test_multiples_of_num_empty_input():
    # Test function with empty input list
    with pytest.raises(TypeError):
        multiples_of_num(None, 5)


def test_multiples_of_num_float_input():
    # Test function with float input
    with pytest.raises(TypeError):
        multiples_of_num(3.5, 6)