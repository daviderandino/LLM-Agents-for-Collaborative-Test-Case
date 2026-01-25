import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('a, expected', [
    (8, True),
    (10, False),
])
def test_is_Power_Of_Two(a, expected):
    assert is_Power_Of_Two(a) == expected

def test_is_Power_Of_Two_zero():
    assert not is_Power_Of_Two(0)

def test_is_Power_Of_Two_negative():
    assert not is_Power_Of_Two(-8)

def test_is_Power_Of_Two_one():
    assert is_Power_Of_Two(1)

@pytest.mark.parametrize('a, b, expected', [
    (8, 8, False),
    (8, 16, True),
    (10, 12, False),
])
def test_differ_At_One_Bit_Pos(a, b, expected):
    assert differ_At_One_Bit_Pos(a, b) == expected

def test_differ_At_One_Bit_Pos_zero():
    assert differ_At_One_Bit_Pos(0, 8) == True

def test_differ_At_One_Bit_Pos_negative():
    assert differ_At_One_Bit_Pos(-8, -16) == True

def test_differ_At_One_Bit_Pos[8-16-True]():
    assert differ_At_One_Bit_Pos(8, 16) == True

def test_differ_At_One_Bit_Pos[8-8-False]():
    assert differ_At_One_Bit_Pos(8, 8) == False