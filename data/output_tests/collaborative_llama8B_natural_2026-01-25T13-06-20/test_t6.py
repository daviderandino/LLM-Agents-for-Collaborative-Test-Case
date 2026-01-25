import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False),
])
def test_is_Power_Of_Two(x, expected):
    assert is_Power_Of_Two(x) == expected

@pytest.mark.parametrize('x, expected', [
    (0, False),
    (1, True),
])
def test_is_Power_Of_Two_boundary(x, expected):
    assert is_Power_Of_Two(x) == expected



# Additional test case to cover the case where both inputs are powers of two
@pytest.mark.parametrize('a, b, expected', [
    (8, 16, False),  # Changed expected to False
    (16, 32, False),  # Changed expected to False
])
def test_differ_At_One_Bit_Pos_powers_of_two(a, b, expected):
    assert differ_At_One_Bit_Pos(a, b) == expected

# Additional test case to cover the case where both inputs are not powers of two
