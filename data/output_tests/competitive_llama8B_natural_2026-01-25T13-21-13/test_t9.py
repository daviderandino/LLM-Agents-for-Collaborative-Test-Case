import pytest
from data.input_code.t9 import *

def test_find_Rotations_non_rotated():
    assert find_Rotations("abc") == 3

def test_find_Rotations_rotated():
    assert find_Rotations("abc") == 3

def test_find_Rotations_single_character():
    assert find_Rotations("a") == 1

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_none_input():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_non_string_input():
    with pytest.raises(TypeError):
        find_Rotations(123)

def test_find_Rotations_zero_length_string():
    assert find_Rotations("") == 0