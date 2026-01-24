import pytest
from data.input_code.t6 import is_Power_Of_Two, differ_At_One_Bit_Pos

def test_is_Power_Of_Two():
    assert is_Power_Of_Two(8) == True
    assert is_Power_Of_Two(10) == False
    assert is_Power_Of_Two(1) == True
    assert is_Power_Of_Two(0) == False



def test_differ_At_One_Bit_Pos_empty():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos([1, 2], [3, 4])

def test_differ_At_One_Bit_Pos_different_types():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(1, '2')



def test_is_Power_Of_Two_floating_point():
    with pytest.raises(TypeError):
        is_Power_Of_Two(1.5)

def test_differ_At_One_Bit_Pos_floating_point():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(1.5, 2)

def test_is_Power_Of_Two_string():
    with pytest.raises(TypeError):
        is_Power_Of_Two('2')

def test_differ_At_One_Bit_Pos_string():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('2', '3')


def test_differ_At_One_Bit_Pos_none():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(2, None)