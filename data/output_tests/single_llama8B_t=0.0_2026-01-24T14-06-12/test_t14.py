import pytest

from data.input_code.t14 import find_Volume


def test_find_Volume_zero():
    # Test with zero
    assert find_Volume(0, 2, 3) == 0.0
    assert find_Volume(1, 0, 3) == 0.0
    assert find_Volume(1, 2, 0) == 0.0


def test_find_Volume_input_types():
    # Test with different input types
    with pytest.raises(TypeError):
        find_Volume("a", 2, 3)
    with pytest.raises(TypeError):
        find_Volume(1, "b", 3)
    with pytest.raises(TypeError):
        find_Volume(1, 2, "c")