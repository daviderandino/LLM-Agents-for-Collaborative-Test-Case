import pytest
from data.input_code.t14 import *

def test_find_Volume_success():
    assert find_Volume(10, 5, 2) == 50.0






def test_find_Volume_non_integer_values():
    assert find_Volume(10.5, 5, 2) == 52.5

def test_find_Volume_non_rectangular_prism():
    assert find_Volume(10, 5, 2.5) == 62.5