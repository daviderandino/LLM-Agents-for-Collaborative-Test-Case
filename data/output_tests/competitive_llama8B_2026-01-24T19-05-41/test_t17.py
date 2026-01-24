import pytest
from data.input_code.t17 import *

@pytest.mark.parametrize('a, expected', [
    (5, 20),
    (0, 0),
    (1000, 4000),
])
def test_square_perimeter_success(a, expected):
    assert square_perimeter(a) == expected

def test_square_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)

def test_square_perimeter_zero():
    assert square_perimeter(0) == 0

