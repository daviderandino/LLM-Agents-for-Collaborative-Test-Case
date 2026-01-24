import pytest

from data.input_code.t14 import find_Volume


def test_find_Volume_invalid_input():
    with pytest.raises(TypeError):
        find_Volume('a', 3, 4)
    with pytest.raises(TypeError):
        find_Volume(2, 'b', 4)
    with pytest.raises(TypeError):
        find_Volume(2, 3, 'c')