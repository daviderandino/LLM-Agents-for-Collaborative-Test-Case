import pytest
from data.input_code.t17 import *

@pytest.mark.parametrize('a, expected', [
    (5, 20),
    (0, 0)
])
def test_square_perimeter_success(a, expected):
    assert square_perimeter(a) == expected



def test_square_perimeter_non_integer():
    assert square_perimeter(3.5) == 14.0