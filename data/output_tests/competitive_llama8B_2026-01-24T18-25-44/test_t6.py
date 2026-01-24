import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False),
    (0, False),
    (-8, False)
])
def test_is_Power_Of_Two(x, expected):
    assert is_Power_Of_Two(x) == expected

def test_is_Power_Of_Two_zero():
    assert is_Power_Of_Two(0) == False


def test_differ_At_One_Bit_Pos_no_difference():
    assert differ_At_One_Bit_Pos(8, 8) == False

def test_differ_At_One_Bit_Pos_more_difference():
    assert differ_At_One_Bit_Pos(8, 9) == True

def test_differ_At_One_Bit_Pos_invalid_input():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 'a')
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 'b')

def test_differ_At_One_Bit_Pos_invalid_input_with_numbers():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 8.5)