import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('input_str, expected', [
    ("abc", 3),
    ("abcd", 4),
])
def test_find_Rotations_success(input_str, expected):
    assert find_Rotations(input_str) == expected


def test_find_Rotations_single_character_string():
    assert find_Rotations("a") == 1

def test_find_Rotations_rotation_found_at_first_position():
    assert find_Rotations("abcabc") == 3

def test_find_Rotations_rotation_not_found():
    assert find_Rotations("abcd") == 4

def test_find_Rotations_rotation_found_at_last_position():
    assert find_Rotations("abcdabcd") == 4

def test_find_Rotations_rotation_found_at_middle_position():
    assert find_Rotations("abcabcab") == 8  # Corrected expected value

def test_find_Rotations_rotation_found_at_middle_position_2():
    assert find_Rotations("abcabcab") == 8  # Corrected expected value