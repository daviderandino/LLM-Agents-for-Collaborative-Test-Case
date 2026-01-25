import pytest
from data.input_code.t14 import *


def test_find_Volume_non_zero_inputs():
    assert find_Volume(10, 5, 2) == 50.0
    assert find_Volume(0, 5, 2) == 0.0
    assert find_Volume(10, 0, 2) == 0.0
    assert find_Volume(0, 5, 0) == 0.0
    assert find_Volume(10, 5, 0) == 0.0
    assert find_Volume(-10, -5, -2) == -50.0
    assert find_Volume(10, -5, 2) == -50.0