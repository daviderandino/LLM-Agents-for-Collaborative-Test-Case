import pytest
from data.input_code.t6 import *

def test_is_Power_Of_Two():
    assert is_Power_Of_Two(8) == True
    assert is_Power_Of_Two(10) == False
    assert is_Power_Of_Two(0) == False
    assert is_Power_Of_Two(-8) == False


def test_differ_At_One_Bit_Pos_error():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 'a') # changed input to non-integer

def test_differ_At_One_Bit_Pos_error2():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('a', 8) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error3():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('a', 'b') # changed input to non-integer

def test_differ_At_One_Bit_Pos_error4():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, None) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error5():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(None, 8) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error6():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(None, None) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error7():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8.5, 7) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error8():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, 7.5) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error9():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8.5, 7.5) # changed input to non-integer




def test_differ_At_One_Bit_Pos_error13():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, [1, 2, 3]) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error14():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos({'a': 1}, 8) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error15():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos((1, 2, 3), 8) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error16():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos('a', (1, 2, 3)) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error17():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos([1, 2, 3], (1, 2, 3)) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error18():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos((1, 2, 3), [1, 2, 3]) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error19():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(8, {'a': 1}) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error20():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos({'a': 1}, {'b': 2}) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error21():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos([1, 2, 3], {'a': 1}) # changed input to non-integer

def test_differ_At_One_Bit_Pos_error22():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos({'a': 1}, [1, 2, 3]) # changed input to non-integer