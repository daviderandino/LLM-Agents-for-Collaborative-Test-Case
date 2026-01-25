import pytest
from data.input_code.t14 import *

@pytest.mark.parametrize('l, b, h, expected', [
    (10, 5, 8, 200.0),
    (0, 5, 8, 0.0),
    (10, 0, 8, 0.0),
    (10, 5, 0, 0.0),
    (10, 5, 8, 200.0),  # Corrected expected value
    (10, -5, 8, -200.0),  # Corrected expected value
    (0, 0, 8, 0.0),
    (0, 5, 8, 0.0),
    (0, 5, 0, 0.0),
])
def test_find_Volume_success(l, b, h, expected):
    assert find_Volume(l, b, h) == expected


def test_find_Volume_non_numeric_input_l():
    with pytest.raises(TypeError):
        find_Volume('a', 5, 8)

def test_find_Volume_non_numeric_input_b():
    with pytest.raises(TypeError):
        find_Volume(10, 'b', 8)

def test_find_Volume_non_numeric_input_h():
    with pytest.raises(TypeError):
        find_Volume(10, 5, 'c')