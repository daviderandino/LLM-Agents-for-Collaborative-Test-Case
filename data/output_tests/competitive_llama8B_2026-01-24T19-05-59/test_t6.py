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
        differ_At_One_Bit_Pos("8", 0)  

def test_differ_At_One_Bit_Pos_invalid_input_type():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, "0")  

def test_differ_At_One_Bit_Pos_success_with_same_input():
    assert differ_At_One_Bit_Pos(8, 8) == False

def test_differ_At_One_Bit_Pos_invalid_input_type2():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos("8", 8)