import pytest
from data.input_code.t14 import *

@pytest.mark.parametrize('l, b, h, expected', [
    (10, 5, 2, 50.0),  # Corrected expected value
    (0, 5, 2, 0.0),
    (10, 0, 2, 0.0),
    (10, 5, 0, 0.0),
    (0, 0, 0, 0.0),
])
def test_find_Volume_success(l, b, h, expected):
    assert find_Volume(l, b, h) == expected

def test_find_Volume_error():
    with pytest.raises(TypeError):
        find_Volume(None, 5, 2)
    with pytest.raises(TypeError):
        find_Volume("a", 5, 2)