import pytest
from dynamic_programming import *

@pytest.mark.parametrize('n, expected', [
    (0, 1),
    (1, 0),
    (2, 2),
    (5, 8),
    (100, 354224848179261915075)
])
def test_count_ways_success(n, expected):
    assert count_ways(n) == expected

def test_count_ways_zero_error():
    with pytest.raises(TypeError):
        count_ways(-1)

def test_count_ways_non_integer_error():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_invalid_input_type():
    with pytest.raises(TypeError):
        count_ways("hello")

def test_count_ways_input_out_of_range_negative_integer():
    with pytest.raises(TypeError):
        count_ways(-100)

def test_count_ways_input_out_of_range_large_integer():
    with pytest.raises(OverflowError):
        count_ways(10**100)

def test_count_ways_input_out_of_range_non_integer():
    with pytest.raises(TypeError):
        count_ways(3.5)