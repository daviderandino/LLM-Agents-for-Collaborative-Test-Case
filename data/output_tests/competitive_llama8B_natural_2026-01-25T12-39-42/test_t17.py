import pytest
from data.input_code.t17 import *
from shapes import *

def test_square_perimeter_positive():
    assert square_perimeter(5) == 20

def test_square_perimeter_zero():
    assert square_perimeter(0) == 0

def test_square_perimeter_negative():
    with pytest.raises(ValueError):
        square_perimeter(-5)

def test_square_perimeter_non_numeric():
    with pytest.raises(TypeError):
        square_perimeter('five')

def test_square_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)

# Removed duplicate tests