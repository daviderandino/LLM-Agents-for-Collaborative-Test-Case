import pytest

from data.input_code.t14 import find_Volume


def test_find_Volume_invalid_input():
    with pytest.raises(TypeError):
        find_Volume('a', 20, 30)
    with pytest.raises(TypeError):
        find_Volume(10, 'b', 30)
    with pytest.raises(TypeError):
        find_Volume(10, 20, 'c')