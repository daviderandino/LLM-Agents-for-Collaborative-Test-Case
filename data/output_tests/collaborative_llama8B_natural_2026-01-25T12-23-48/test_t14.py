import pytest
from data.input_code.t14 import *



def test_find_Volume_non_numeric_input():
    with pytest.raises(TypeError):
        find_Volume("10", 5, 3)
    with pytest.raises(TypeError):
        find_Volume(10, "5", 3)
    with pytest.raises(TypeError):
        find_Volume(10, 5, "3")

def test_find_Volume_all_zero():
    assert find_Volume(0, 0, 0) == 0.0