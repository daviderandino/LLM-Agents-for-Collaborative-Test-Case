import pytest
from data.input_code.t5 import *



def test_count_ways_error_non_integer():
    with pytest.raises(TypeError):
        count_ways(2.5)

