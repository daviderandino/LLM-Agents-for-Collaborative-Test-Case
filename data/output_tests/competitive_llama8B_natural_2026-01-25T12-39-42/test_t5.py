import pytest
from data.input_code.t5 import *


def test_count_ways_error():
    with pytest.raises(IndexError):
        count_ways(-1)

def test_count_ways_non_integer():
    with pytest.raises(TypeError):
        count_ways(2.5)

def test_count_ways_non_integer_0_5():
    with pytest.raises(TypeError):
        count_ways(0.5)

def test_count_ways_recursion_edge_case_2():
    assert count_ways(2) == 3


def test_count_ways_recursion_general():
    n = 4
    A = [0] * (n + 1) 
    B = [0] * (n + 1) 
    A[0] = 1
    A[1] = 0
    B[0] = 0
    B[1] = 1
    for i in range(2, n+1): 
        A[i] = A[i - 2] + 2 * B[i - 1] 
        B[i] = A[i - 1] + B[i - 2] 
    assert count_ways(n) == A[n]