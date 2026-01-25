import pytest
from data.input_code.t9 import *

def test_find_Rotations_single_character():
    assert find_Rotations("a") == 1

def test_find_Rotations_short_string():
    assert find_Rotations("ab") == 2

def test_find_Rotations_medium_length_string():
    assert find_Rotations("abc") == 3


def test_find_Rotations_no_rotation_found():
    assert find_Rotations("abcde" + "f") == len("abcde" + "f")

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_invalid_input_none():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_invalid_input_integer():
    with pytest.raises(TypeError):
        find_Rotations(123)

def test_find_Rotations_invalid_input_float():
    with pytest.raises(TypeError):
        find_Rotations(3.14)