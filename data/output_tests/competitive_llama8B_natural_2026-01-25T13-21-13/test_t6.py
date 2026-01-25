import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False),
    (0, False),
    (-8, False),
    (1, True)
])
def test_is_Power_Of_Two(x, expected):
    assert is_Power_Of_Two(x) == expected

@pytest.mark.parametrize('a, b, expected', [
    (12, 8, True),
    (12, 10, False),
    (8, 10, True),
    (8, 16, False)  # Corrected expected value
])
def test_differ_At_One_Bit_Pos(a, b, expected):
    assert differ_At_One_Bit_Pos(a, b) == expected