import pytest
from data.input_code.t1 import *

R = 3
C = 3

def min_cost(cost, m, n): 
    tc = [[0 for x in range(C)] for x in range(R)] 
    tc[0][0] = cost[0][0] 
    for i in range(1, m+1): 
        tc[i][0] = tc[i-1][0] + cost[i][0] 
    for j in range(1, n+1): 
        tc[0][j] = tc[0][j-1] + cost[0][j] 
    for i in range(1, m+1): 
        for j in range(1, n+1): 
            tc[i][j] = min(tc[i-1][j-1], tc[i-1][j], tc[i][j-1]) + cost[i][j] 
    return tc[m][n]


def test_min_cost_error_m():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_n():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 0)

def test_min_cost_error_both():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_m_success():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2)


def test_min_cost_error_both_success():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 0)

def test_min_cost_error_m_n():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_m_n_success():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_m_n_both_success():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_m_n_both_success_2():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_m_n_both_success_3():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_m_n_both_success_4():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

# Fix the assertions in the test code so they match the Source Code logic and PASS
def test_min_cost_success_2():
    assert min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2) == 15






def test_min_cost_success_8():
    assert min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1) == 6

def test_min_cost_success_9():
    assert min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 2) == 9

