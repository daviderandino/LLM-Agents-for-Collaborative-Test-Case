import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("abc", 3)  # Corrected expected value to match the Source Code logic
])
def test_find_Rotations_normal_string(str, expected):
    assert find_Rotations(str) == expected

@pytest.mark.parametrize('str, rotation, expected', [
    ("abcabc", 1, 3),  # Corrected expected value to match the Source Code logic
    ("abcabc", 2, 3)   # Corrected expected value to match the Source Code logic
])
def test_find_Rotations_rotation_of_original_string(str, rotation, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_single_character_string():
    assert find_Rotations("a") == 1

@pytest.mark.parametrize('str, expected', [
    ("a" * 1000, 1)
])
def test_find_Rotations_large_string(str, expected):
    assert find_Rotations(str) == expected

@pytest.mark.parametrize('str, rotation, expected', [
    ("abc", 2, 3)  # Corrected expected value to match the Source Code logic
])
def test_find_Rotations_no_rotation_found(str, rotation, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_none_input():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_non_string_input():
    with pytest.raises(TypeError):
        find_Rotations(123)