import pytest
from data.input_code.t17 import *
from shapes import *

@pytest.mark.parametrize('a, expected', [
    (10, 40),
    (0, 0),
    (-10, -40)
])
def test_square_perimeter_positive(a, expected):
    assert square_perimeter(a) == expected

def test_square_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)

def test_square_perimeter_non_numeric():
    with pytest.raises(TypeError):
        square_perimeter('a')

def test_square_perimeter_zero():
    assert square_perimeter(0) == 0

def test_square_perimeter_negative():
    assert square_perimeter(-10) == -40

def test_square_perimeter_non_integer():
    assert square_perimeter(10.5) == 42.0

def test_square_perimeter_string():
    with pytest.raises(TypeError):
        square_perimeter('a')

def test_square_perimeter_list():
    with pytest.raises(TypeError):
        square_perimeter([10])

def test_square_perimeter_dict():
    with pytest.raises(TypeError):
        square_perimeter({'a': 10})

def test_square_perimeter_boolean():
    with pytest.raises(TypeError):
        square_perimeter(True)

def test_square_perimeter_float():
    assert square_perimeter(10.5) == 42.0

def test_square_perimeter_tuple():
    with pytest.raises(TypeError):
        square_perimeter((10,))

def test_square_perimeter_set():
    with pytest.raises(TypeError):
        square_perimeter({10})

def test_square_perimeter_complex():
    with pytest.raises(TypeError):
        square_perimeter(10+10j)

def test_square_perimeter_invalid_input():
    with pytest.raises(TypeError):
        square_perimeter(10)