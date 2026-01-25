import pytest
from data.input_code.t5 import *




def test_count_ways_non_integer():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_non_numeric():
    with pytest.raises(TypeError):
        count_ways('hello')