import pytest
from data.input_code.t1 import *

R = 3
C = 3






def test_min_cost_error_non_integer_rows():
    with pytest.raises(TypeError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2.5, 2)

def test_min_cost_error_non_integer_cols():
    with pytest.raises(TypeError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2.5)

def test_min_cost_error_m_larger_than_rows():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2)

def test_min_cost_error_n_larger_than_cols():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3)

def test_min_cost_error_m_larger_than_m():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2)

def test_min_cost_error_n_larger_than_n():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3)

def test_min_cost_error_m_larger_than_cols():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3)

def test_min_cost_error_n_larger_than_rows():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3)

def test_min_cost_error_m_and_n_larger_than_rows_and_cols():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)

def test_min_cost_error_m_larger_than_m():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2)

def test_min_cost_error_n_larger_than_n():
    with pytest.raises(IndexError):
        min_cost([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3)

# Fix the assertions in the test code so they match the Source Code logic and PASS


