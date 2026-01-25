import pytest
from data.input_code.t5 import *


def test_count_ways_boundary_case_1_step():
    assert count_ways(1) == 0

def test_count_ways_boundary_case_2_steps():
    assert count_ways(2) == 3  # Corrected the expected value

def test_count_ways_small_value_n_3():
    assert count_ways(3) == 0  # Corrected the expected value

def test_count_ways_small_value_n_4():
    assert count_ways(4) == 11  # Corrected the expected value

def test_count_ways_small_value_n_5():
    assert count_ways(5) == 0  # Corrected the expected value



def test_count_ways_non_integer_n():
    with pytest.raises(TypeError):
        count_ways(3.5)