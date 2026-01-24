import pytest
from data.input_code.t5 import *


def test_count_ways_large_input():
    result = count_ways(100)
    assert result == 31208688988045323113527764971


def test_count_ways_non_integer_input():
    with pytest.raises(TypeError):
        count_ways(3.5)



def test_count_ways_positive_input():
    result = count_ways(10)
    assert result == 571



