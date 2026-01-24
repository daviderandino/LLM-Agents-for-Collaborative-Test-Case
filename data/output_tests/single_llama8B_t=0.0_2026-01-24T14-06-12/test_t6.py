import pytest
from data.input_code.t6 import is_Power_Of_Two, differ_At_One_Bit_Pos

def test_is_Power_Of_Two_success():
    assert is_Power_Of_Two(8) == True
    assert is_Power_Of_Two(16) == True
    assert is_Power_Of_Two(32) == True

def test_is_Power_Of_Two_edge_cases():
    assert is_Power_Of_Two(0) == False
    assert is_Power_Of_Two(1) == True
    assert is_Power_Of_Two(-1) == False
    assert is_Power_Of_Two(-8) == False

def test_is_Power_Of_Two_negative_numbers():
    with pytest.raises(TypeError):
        is_Power_Of_Two(-8.5)


def test_differ_At_One_Bit_Pos_edge_cases():
    assert differ_At_One_Bit_Pos(0, 0) == False
    assert differ_At_One_Bit_Pos(1, 1) == False
    assert differ_At_One_Bit_Pos(8, 8) == False
    assert differ_At_One_Bit_Pos(16, 16) == False


def test_differ_At_One_Bit_Pos_invalid_input():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('a', 'b')