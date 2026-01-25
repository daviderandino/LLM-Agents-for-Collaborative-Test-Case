import pytest
from data.input_code.t14 import *


def test_find_Volume_error():
    with pytest.raises(TypeError):
        find_Volume('a', 5, 2)
    with pytest.raises(TypeError):
        find_Volume(10, 'b', 2)
    with pytest.raises(TypeError):
        find_Volume(10, 5, 'c')