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


def test_differ_At_One_Bit_Pos_error():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 0.5) # Changed to a float input

def test_differ_At_One_Bit_Pos_type_error():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(0.5, 8) # Added a float input

def test_differ_At_One_Bit_Pos_invalid_input():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos("8", 8) # Added a string input