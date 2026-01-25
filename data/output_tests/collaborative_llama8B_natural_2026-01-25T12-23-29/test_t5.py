import pytest
from data.input_code.t5 import *



def test_count_ways_non_integer_error():
    with pytest.raises(TypeError):
        count_ways(2.5)

def test_count_ways_return_list():
    result = count_ways(1)
    assert isinstance(result, int)
    with pytest.raises(TypeError):
        count_ways(1, return_lists=True)




def test_count_ways_non_integer_input():
    with pytest.raises(TypeError):
        count_ways(2.5)

def test_count_ways_return_type():
    result = count_ways(1)
    assert isinstance(result, int)
    with pytest.raises(TypeError):
        count_ways(1, return_lists=True)








