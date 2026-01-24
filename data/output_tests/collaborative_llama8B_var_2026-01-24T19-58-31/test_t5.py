import pytest
from data.input_code.t5 import *


def test_count_ways_error():
    with pytest.raises(IndexError):
        count_ways(-1)

def test_count_ways_non_int():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_non_positive():
    with pytest.raises(IndexError):
        count_ways(0)


def test_count_ways_one():
    A = [0] * (1 + 1)
    B = [0] * (1 + 1)
    A[0] = 1
    A[1] = 0
    B[0] = 0
    B[1] = 1
    count_ways(1)
    assert A[1] == 0
    assert B[1] == 1


def test_count_ways_non_positive_setup():
    with pytest.raises(IndexError):
        count_ways(0)

def test_count_ways_non_int_setup():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_error_setup():
    with pytest.raises(IndexError):
        count_ways(-1)