import pytest
from data.input_code.t6 import *

def test_is_Power_Of_Two():
    assert is_Power_Of_Two(8)
    assert not is_Power_Of_Two(10)
    assert not is_Power_Of_Two(0)
    assert not is_Power_Of_Two(-8)


def test_differ_At_One_Bit_Pos_error():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 'a')

def test_differ_At_One_Bit_Pos_error2():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, None)


def test_differ_At_One_Bit_Pos_error4():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 8.5)

def test_differ_At_One_Bit_Pos_error5():
    # This should not raise TypeError
    differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error6():
    # This should not raise TypeError
    differ_At_One_Bit_Pos(8, 0)