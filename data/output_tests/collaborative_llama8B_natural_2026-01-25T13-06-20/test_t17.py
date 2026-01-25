import pytest
from data.input_code.t17 import *

def test_square_perimeter_success():
    pytest.raises(AssertionError, lambda: square_perimeter(-5))
    pytest.raises(AssertionError, lambda: square_perimeter('a'))

@pytest.mark.parametrize('a, expected', [
    (5, 20),
    (0, 0),
    (1000000, 4000000),
    (0.01, 0.04)
])
def test_square_perimeter_success(a, expected):
    assert square_perimeter(a) == expected