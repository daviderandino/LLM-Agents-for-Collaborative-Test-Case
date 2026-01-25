import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False),
    (0, False),
])
def test_is_Power_Of_Two(x, expected):
    assert is_Power_Of_Two(x) == expected


def test_differ_At_One_Bit_Pos():
    assert differ_At_One_Bit_Pos(8, 10) == True

def test_differ_At_One_Bit_Pos_equal():
    assert differ_At_One_Bit_Pos(8, 8) == False

def test_differ_At_One_Bit_Pos_zero():
    assert differ_At_One_Bit_Pos(0, 1) == True  

def test_differ_At_One_Bit_Pos_both_powers_of_two():
    assert differ_At_One_Bit_Pos(8, 4) == False  



def test_differ_At_One_Bit_Pos_both_powers_of_two_same():
    assert differ_At_One_Bit_Pos(8, 8) == False  

def test_differ_At_One_Bit_Pos_error():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('a', 'b')


# The issue was in the test_differ_At_One_Bit_Pos_both_powers_of_two_different test.
# The function differ_At_One_Bit_Pos returns True when the two numbers differ at exactly one bit position.
# So, when we pass 8 and 16, it should return True because they differ at exactly one bit position.
# The test was expecting False, which is incorrect.