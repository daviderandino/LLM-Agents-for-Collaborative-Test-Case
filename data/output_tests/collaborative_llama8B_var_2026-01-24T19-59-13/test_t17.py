import pytest
from shapes import *

@pytest.mark.parametrize('a, expected', [
    (5, 20),
    (0, 0),
    (1000, 4000),
    (-5, 20)
])
def test_square_perimeter_success(a, expected):
    assert square_perimeter(a) == expected

def test_square_perimeter_non_numeric():
    with pytest.raises(TypeError):
        square_perimeter("five")

def test_square_perimeter_non_positive():
    with pytest.raises(ValueError):
        square_perimeter(-5)

def test_square_perimeter_non_integer():
    with pytest.raises(TypeError):
        square_perimeter(5.5)