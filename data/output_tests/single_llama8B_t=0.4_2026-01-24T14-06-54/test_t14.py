import pytest

from data.input_code.t14 import find_Volume

def test_find_Volume_success():
    # Test with positive numbers
    assert find_Volume(10, 5, 2) == (10 * 5 * 2) / 2
    assert find_Volume(15, 10, 3) == (15 * 10 * 3) / 2

def test_find_Volume_zero():
    # Test with zero
    assert find_Volume(0, 5, 2) == 0
    assert find_Volume(15, 0, 3) == 0
    assert find_Volume(10, 5, 0) == 0


def test_find_Volume_invalid_input():
    # Test with non-numeric input
    with pytest.raises(TypeError):
        find_Volume('10', 5, 2)
    with pytest.raises(TypeError):
        find_Volume(10, '5', 2)
    with pytest.raises(TypeError):
        find_Volume(10, 5, '2')