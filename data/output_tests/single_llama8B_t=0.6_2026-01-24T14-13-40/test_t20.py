import pytest
from data.input_code.t20 import multiples_of_num




def test_multiples_of_num_non_integer():
    # Test non-integer input
    with pytest.raises(TypeError):
        multiples_of_num(5.5, 3)
    with pytest.raises(TypeError):
        multiples_of_num(5, 3.5)