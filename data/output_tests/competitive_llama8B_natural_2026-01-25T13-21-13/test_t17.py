import pytest
from data.input_code.t17 import *

@pytest.mark.parametrize('a, expected', [
    (5, 20.0),
    (0, 0.0),
    (0.1, 0.4)
])
def test_square_perimeter_success(a, expected):
    result = square_perimeter(a)
    assert result == expected


