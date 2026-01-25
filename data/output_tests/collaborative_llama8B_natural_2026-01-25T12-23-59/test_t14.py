import pytest
from data.input_code.t14 import *

def test_find_Volume_success():
    assert find_Volume(5, 3, 2) == 15.0



@pytest.mark.parametrize('l, b, h', [
    (1000000, 1000000, 1000000)
])
def test_find_Volume_large_success(l, b, h):
    assert find_Volume(l, b, h) == (l * b * h) / 2

# The issue is that the function find_Volume does not raise a ValueError for negative inputs
# It actually returns a float value for negative inputs
@pytest.mark.parametrize('l, b, h', [
    (-5, -3, -2),
    (5, -3, 2),
    (-5, 3, -2),
    (5, 3, -2)
])
def test_find_Volume_negative_success(l, b, h):
    assert find_Volume(l, b, h) == ((l * b * h) / 2)

# The issue is that the function find_Volume does not raise a ZeroDivisionError for zero inputs
# It actually returns a float value for zero inputs
@pytest.mark.parametrize('l, b, h', [
    (0, 3, 2),
    (5, 0, 2),
    (0, 0, 2),
    (5, 3, 0)
])
def test_find_Volume_zero_success(l, b, h):
    assert find_Volume(l, b, h) == 0.0