import pytest
from data.input_code.t5 import *


def test_count_ways_one():
    assert count_ways(1) == 0



def test_count_ways_large_positive():
    assert count_ways(10) == 571


def test_count_ways_non_integer_input():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_non_numeric_input():
    with pytest.raises(TypeError):
        count_ways("hello")