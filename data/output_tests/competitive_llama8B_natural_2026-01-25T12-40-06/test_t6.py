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

def test_is_Power_Of_Two_one():
    assert is_Power_Of_Two(1) == True

def test_is_Power_Of_Two_negative():
    assert is_Power_Of_Two(-8) == False

def test_is_Power_Of_Two_float():
    with pytest.raises(TypeError):
        is_Power_Of_Two(4.0)

def test_is_Power_Of_Two_non_integer():
    with pytest.raises(TypeError):
        is_Power_Of_Two(4.5)

@pytest.mark.parametrize('a, b, expected', [
    (8, 4, False),
    (10, 8, True),
    (12, 8, True),
    (16, 8, False),
])
def test_differ_At_One_Bit_Pos(a, b, expected):
    assert differ_At_One_Bit_Pos(a, b) == expected