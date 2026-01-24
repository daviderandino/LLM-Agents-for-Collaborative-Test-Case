import pytest

from data.input_code.t14 import find_Volume


def test_find_Volume_invalid_input():
    with pytest.raises(TypeError):
        find_Volume(1, None, 1)
    with pytest.raises(TypeError):
        find_Volume(None, 1, 1)
    with pytest.raises(TypeError):
        find_Volume(None, None, None)