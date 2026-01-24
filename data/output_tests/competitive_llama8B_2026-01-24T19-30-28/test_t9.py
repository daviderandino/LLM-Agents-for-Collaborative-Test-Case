import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("abc", 3),
    ("abcd", 4),
])
def test_find_Rotations_success(str, expected):
    assert find_Rotations(str) == expected


def test_find_Rotations_single_character_string():
    assert find_Rotations("a") == 1

def test_find_Rotations_long_string():
    assert find_Rotations("abcdefgh") == 8

def test_find_Rotations_equal_to_length():
    assert find_Rotations("abcdabcd") == 4