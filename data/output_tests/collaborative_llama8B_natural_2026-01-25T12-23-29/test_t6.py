import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False),
])
def test_is_Power_Of_Two(x, expected):
    assert is_Power_Of_Two(x) == expected

def test_is_Power_Of_Two_zero():
    assert is_Power_Of_Two(0) == False

def test_is_Power_Of_Two_negative():
    assert is_Power_Of_Two(-8) == False


# Test differ_At_One_Bit_Pos with correct expected values
