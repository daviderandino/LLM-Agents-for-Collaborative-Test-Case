import pytest
from data.input_code.t9 import *

def test_find_Rotations_single_character():
    assert find_Rotations("a") == 1

def test_find_Rotations_two_characters():
    assert find_Rotations("ab") == 2

def test_find_Rotations_string_rotation():
    assert find_Rotations("abcabc") == 3

def test_find_Rotations_three_characters():
    assert find_Rotations("abc") == 3

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_none_input():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_large_string():
    assert find_Rotations("a"*1000) == 1

def test_find_Rotations_non_rotation():
    assert find_Rotations("abcd") == 4

def test_find_Rotations_special_characters():
    assert find_Rotations("a!b@c") == 5