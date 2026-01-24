import pytest
from data.input_code.t14 import find_Volume

def test_find_Volume_success():
    assert find_Volume(1, 2, 3) == 3

def test_find_Volume_zero():
    assert find_Volume(0, 2, 3) == 0


def test_find_Volume_non_numeric():
    with pytest.raises(TypeError):
        find_Volume("a", 2, 3)

def test_find_Volume_empty_args():
    with pytest.raises(TypeError):
        find_Volume()