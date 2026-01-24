import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("abc", 3),
    ("abcd", 4),
])
def test_find_Rotations_success(str, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_single_character_string():
    assert find_Rotations("a") == 1