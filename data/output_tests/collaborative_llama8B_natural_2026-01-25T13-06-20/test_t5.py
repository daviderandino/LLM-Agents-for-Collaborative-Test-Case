import pytest
from staircase import *

@pytest.mark.parametrize('n, expected', [
    (1, 1),
    (2, 1),
    (5, 13),
    (0, 1)
])
def test_count_ways_success(n, expected):
    assert count_ways(n) == expected

def test_count_ways_large_input():
    assert count_ways(100) == 354224848179261915075

def test_count_ways_negative_input():
    with pytest.raises(ValueError):
        count_ways(-1)

def test_count_ways_non_integer_input():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_zero_input():
    assert count_ways(0) == 1