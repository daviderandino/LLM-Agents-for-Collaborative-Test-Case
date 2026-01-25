import pytest
from data.input_code.t6 import *

def test_is_Power_Of_Two_power_of_2():
    assert is_Power_Of_Two(8)

def test_is_Power_Of_Two_non_power_of_2():
    assert not is_Power_Of_Two(6)

def test_is_Power_Of_Two_zero():
    assert not is_Power_Of_Two(0)

def test_is_Power_Of_Two_negative():
    assert not is_Power_Of_Two(-8)

def test_is_Power_Of_Two_non_integer():
    with pytest.raises(TypeError):
        is_Power_Of_Two(3.5)

def test_is_Power_Of_Two_non_numeric():
    with pytest.raises(TypeError):
        is_Power_Of_Two('hello')

def test_differ_At_One_Bit_Pos_both_powers_of_2():
    assert not differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_one_power_of_2():
    assert differ_At_One_Bit_Pos(8, 10)


def test_differ_At_One_Bit_Pos_zero():
    assert differ_At_One_Bit_Pos(0, 8)


def test_differ_At_One_Bit_Pos_non_integer():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(3.5, 8)

def test_differ_At_One_Bit_Pos_non_numeric():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('hello', 8)




