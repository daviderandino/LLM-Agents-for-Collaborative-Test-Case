import pytest
from data.input_code.t14 import *

def test_find_Volume_success():
    @pytest.mark.parametrize('l, b, h, expected', [
        (10, 5, 2, 50.0),
        (0, 5, 2, 0.0),
        (10, 0, 2, 0.0),
        (10, 5, 0, 0.0),
        (100, 50, 20, 50000.0),
        (-10, 5, 2, -50.0),
        (10, -5, 2, -50.0),
        (10, 5, -2, -50.0),
        (0, 0, 0, 0.0),
    ])
    def _test(l, b, h, expected):
        assert find_Volume(l, b, h) == expected

def test_find_Volume_error_none_input():
    with pytest.raises(TypeError):
        find_Volume(None, 5, 2)
    with pytest.raises(TypeError):
        find_Volume(10, None, 2)
    with pytest.raises(TypeError):
        find_Volume(10, 5, None)