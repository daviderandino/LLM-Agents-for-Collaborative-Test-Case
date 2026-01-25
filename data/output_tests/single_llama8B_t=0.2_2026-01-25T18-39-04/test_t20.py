import pytest
from data.input_code.t20 import multiples_of_num




def test_multiples_of_num_invalid_input():
    # Test with invalid input types
    with pytest.raises(TypeError):
        multiples_of_num('a', 2)
    with pytest.raises(TypeError):
        multiples_of_num(5, 'b')


