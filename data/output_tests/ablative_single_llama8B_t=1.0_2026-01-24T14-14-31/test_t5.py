import pytest

from data.input_code.t5 import count_ways

@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 0),
    (2, 2),
    (3, 4),
    (4, 7),
])
def test_count_ways(n, expected):
    assert count_ways(n) == expected

def test_count_ways_edge_cases():
    with pytest.raises IndexError:  # edge case: n < 0
        count_ways(-1)

def test_count_ways_zero():
    assert count_ways(0) == 1  # zero is a special case
    assert count_ways(-0) == 1  # zero is a special case
    assert count_ways(0.0) == 1  # zero is a special case

def test_count_ways_none():
    with pytest.raises(TypeError):  # n should be an integer
        count_ways(None)

def test_count_ways_large_input():
    # large input to confirm recursive calculation works
    n = 100
    assert count_ways(n) >= 0  # ensure count is non-negative