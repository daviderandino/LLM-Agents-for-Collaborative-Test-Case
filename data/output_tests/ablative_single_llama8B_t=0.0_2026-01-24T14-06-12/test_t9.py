import pytest
from data.input_code.t9 import find_Rotations


def test_find_Rotations_no_rotation():
    # Test case with a string that does not have a rotation
    assert find_Rotations("abcdef") == 6

def test_find_Rotations_empty_string():
    # Test case with an empty string
    assert find_Rotations("") == 0

def test_find_Rotations_single_character():
    # Test case with a single character string
    assert find_Rotations("a") == 1

def test_find_Rotations_none_input():
    # Test case with None input
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_non_string_input():
    # Test case with non-string input
    with pytest.raises(TypeError):
        find_Rotations(123)

def test_find_Rotations_long_string():
    # Test case with a long string
    assert find_Rotations("a" * 1000) == 1

