import pytest
from data.input_code.t14 import *

@pytest.mark.parametrize('l, b, h, expected', [
    (5, 3, 2, 15.0),
    (0, 3, 2, 0.0),
    (0, 0, 2, 0.0),
    (5, 3, 0, 0.0),
    (-5, -3, -2, -15.0),
    (5, -3, -2, 15.0),
    (1000000, 3, 2, 3000000.0),  # Corrected expected value
    (1e-06, 3e-06, 2e-06, 3e-18),  # Corrected expected value
])
def test_find_Volume_success(l, b, h, expected):
    assert find_Volume(l, b, h) == expected


def test_find_Volume_non_numeric_dimensions():
    with pytest.raises(TypeError):
        find_Volume('a', 3, 2)