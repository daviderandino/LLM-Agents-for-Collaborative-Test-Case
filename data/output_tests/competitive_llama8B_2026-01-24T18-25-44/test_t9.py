import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("abc", 3),
    ("abcd", 4)
])
def test_find_Rotations_success(str, expected):
    assert find_Rotations(str) == expected

@pytest.mark.parametrize('str, expected', [
    ("", 0),
    ("a", 1)
])
def test_find_Rotations_empty_or_single_character(str, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_empty_string():
    with pytest.raises(TypeError):
        find_Rotations(None)