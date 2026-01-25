import pytest
from data.input_code.t14 import *


def test_find_Volume_non_numeric_input():
    with pytest.raises(TypeError):
        find_Volume('a', 3, 2)
    with pytest.raises(TypeError):
        find_Volume(5, 'b', 2)
    with pytest.raises(TypeError):
        find_Volume(5, 3, 'c')

def test_find_Volume_success():
    pytest.raises(TypeError, find_Volume, 'a', 3, 2)
    pytest.raises(TypeError, find_Volume, 5, 'b', 2)
    pytest.raises(TypeError, find_Volume, 5, 3, 'c')

def test_find_Volume_zero_volume():
    assert find_Volume(0, 3, 2) == 0.0
    assert find_Volume(5, 0, 2) == 0.0
    assert find_Volume(5, 3, 0) == 0.0