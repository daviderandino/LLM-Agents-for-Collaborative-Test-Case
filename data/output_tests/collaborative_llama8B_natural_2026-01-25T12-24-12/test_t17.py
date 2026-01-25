import pytest
from data.input_code.t17 import *


def test_square_perimeter_large_input():
    assert square_perimeter(1000000) == 4000000

def test_square_perimeter_none_input():
    with pytest.raises(TypeError):
        square_perimeter(None)