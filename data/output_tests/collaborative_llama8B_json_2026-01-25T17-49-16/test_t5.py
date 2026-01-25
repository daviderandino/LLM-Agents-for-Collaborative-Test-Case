import pytest
from data.input_code.t5 import *



def test_count_ways_non_integer():
    with pytest.raises(TypeError):
        count_ways(3.5)



def test_count_ways_one():
    assert count_ways(1) == 0







def test_count_ways_invalid_input_non_integer():
    with pytest.raises(TypeError):
        count_ways(3.5)





