import pytest
from data.input_code.t17 import *


def test_square_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)