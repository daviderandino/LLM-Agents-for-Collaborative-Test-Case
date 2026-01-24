import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False),
    (0, False),
    (-8, False)
])
def test_is_Power_Of_Two(x, expected):
    result = is_Power_Of_Two(x)
    assert result == expected

def test_is_Power_Of_Two_zero():
    assert is_Power_Of_Two(0) == False


def test_differ_At_One_Bit_Pos_no_difference():
    assert differ_At_One_Bit_Pos(8, 8) == False

def test_differ_At_One_Bit_Pos_more_difference():
    assert differ_At_One_Bit_Pos(8, 9) == True

def test_differ_At_One_Bit_Pos_invalid_input():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 'a')  # changed input to a non-integer value

def test_differ_At_One_Bit_Pos_same_input():
    assert differ_At_One_Bit_Pos(8, 8) == False

def test_differ_At_One_Bit_Pos_invalid_inputs():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('a', 8)  # changed input to a non-integer value