import pytest
from data.input_code.t17 import *

@pytest.mark.parametrize('a, expected', [
    (4, 16),
    (0, 0),
    (100, 400),
    (-5, -20)
])
def test_square_perimeter_success(a, expected):
    assert square_perimeter(a) == expected

def test_square_perimeter_error():
    with pytest.raises(TypeError):
        square_perimeter(None)



def test_square_perimeter_dict():
    with pytest.raises(TypeError):
        square_perimeter({'a': 1})


def test_square_perimeter_zero():
    assert square_perimeter(0) == 0


# Fixing the failing tests


def test_square_perimeter_dict_typeerror():
    with pytest.raises(TypeError):
        square_perimeter({'a': 1})


