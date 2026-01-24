import pytest
from data.input_code.t20 import *


def test_multiples_of_num_zero_divisor():
    with pytest.raises(ValueError):
        multiples_of_num(5, 0)