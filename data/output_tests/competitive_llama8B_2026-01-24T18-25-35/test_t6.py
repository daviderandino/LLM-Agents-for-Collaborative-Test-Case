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

def test_is_Power_Of_Two_edge_cases():
    assert is_Power_Of_Two(1) == True
    assert is_Power_Of_Two(2) == True
    assert is_Power_Of_Two(4) == True
    assert is_Power_Of_Two(16) == True


def test_differ_At_One_Bit_Pos_error():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, '8')  # inputs are of different types, TypeError should be raised
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('8', 8)  # inputs are of different types, TypeError should be raised

def test_differ_At_One_Bit_Pos_input_type():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 8.5)  # inputs are of different types, TypeError should be raised
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8.5, 8)  # inputs are of different types, TypeError should be raised