import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('input_str, expected', [
    ("abcabc", 3),
    ("abcdabcd", 4)
])
def test_find_Rotations_success(input_str, expected):
    assert find_Rotations(input_str) == expected

def test_find_Rotations_no_rotation():
    assert find_Rotations("abc") == 3

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_none_input():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_non_string_input():
    with pytest.raises(TypeError):
        find_Rotations(123)