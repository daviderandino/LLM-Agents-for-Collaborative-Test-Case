import pytest

from data.input_code.t9 import find_Rotations

def test_find_Rotations_zero_length_string():
    assert find_Rotations("") == 0

def test_find_Rotations_single_character_string():
    assert find_Rotations("a") == 1


def test_find_Rotations_non_rotated_string():
    assert find_Rotations("abcd") == 4



def test_find_Rotations_input_not_string():
    with pytest.raises(TypeError):
        find_Rotations(123)

