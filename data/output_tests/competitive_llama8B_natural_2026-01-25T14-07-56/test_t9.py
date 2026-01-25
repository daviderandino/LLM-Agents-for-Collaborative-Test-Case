import pytest
from data.input_code.t9 import *

def test_find_Rotations_rotation_found():
    assert find_Rotations("abcde") == 5

def test_find_Rotations_no_rotation_found():
    assert find_Rotations("abcdefg") == 7

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_single_character():
    assert find_Rotations("a") == 1

def test_find_Rotations_power_of_2():
    assert find_Rotations("abcdefghi") == 9

def test_find_Rotations_rotation_at_end():
    assert find_Rotations("abcdefgabcdefg") == 7


def test_find_Rotations_invalid_input_type():
    with pytest.raises(TypeError):
        find_Rotations(123)

def test_find_Rotations_none_input():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_rotation_at_beginning_correct():
    assert find_Rotations("abcdefgabcde") == 12

def test_find_Rotations_rotation_at_end_correct():
    assert find_Rotations("abcdefgabcdefg") == 7