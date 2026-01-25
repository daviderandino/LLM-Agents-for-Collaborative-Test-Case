import pytest
from data.input_code.t9 import find_Rotations


def test_find_Rotations_not_a_rotation():
    # Test case for a string that is not a rotation of itself
    assert find_Rotations("abcde") == 5

def test_find_Rotations_empty_string():
    # Test case for an empty string
    assert find_Rotations("") == 0

def test_find_Rotations_single_character():
    # Test case for a single character string
    assert find_Rotations("a") == 1


def test_find_Rotations_none_input():
    # Test case for None input
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_non_string_input():
    # Test case for non-string input
    with pytest.raises(TypeError):
        find_Rotations(123)


