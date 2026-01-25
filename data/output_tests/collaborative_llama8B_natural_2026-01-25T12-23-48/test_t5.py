import pytest
from dp import *

def test_count_ways_zero_stairs():
    assert count_ways(0) == 1

def test_count_ways_one_stair():
    assert count_ways(1) == 0

def test_count_ways_two_stairs():
    assert count_ways(2) == 2

def test_count_ways_small_number_of_stairs():
    assert count_ways(3) == 4

def test_count_ways_large_number_of_stairs():
    assert count_ways(10) == 89

def test_count_ways_negative_number_of_stairs():
    with pytest.raises(ValueError):
        count_ways(-1)

def test_count_ways_non_integer_number_of_stairs():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_large_number_of_stairs_edge_case():
    assert count_ways(10000) == 269715485

def test_count_ways_power_of_two_stairs():
    assert count_ways(16) == 1493

def test_count_ways_power_of_three_stairs():
    assert count_ways(27) == 109946942