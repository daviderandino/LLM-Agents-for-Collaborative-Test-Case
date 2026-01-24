import pytest
from data.input_code.t6 import is_Power_Of_Two, differ_At_One_Bit_Pos

def test_is_Power_Of_Two_success():
    assert is_Power_Of_Two(2**5)
    assert is_Power_Of_Two(2**3)

def test_is_Power_Of_Two_empty():
    assert not is_Power_Of_Two(0)
    assert not is_Power_Of_Two(None)
    assert not is_Power_Of_Two("")

def test_is_Power_Of_Two_negative():
    assert not is_Power_Of_Two(-1)
    assert not is_Power_Of_Two(-2**3)



def test_differ_At_One_Bit_Pos_no_difference():
    assert not differ_At_One_Bit_Pos(2**3, 2**4)
    assert not differ_At_One_Bit_Pos(2, 2)

def test_differ_At_One_Bit_Pos_no_power_of_two():
    assert not differ_At_One_Bit_Pos(2**2, 3)
    assert not differ_At_One_Bit_Pos(2**5, -1)

