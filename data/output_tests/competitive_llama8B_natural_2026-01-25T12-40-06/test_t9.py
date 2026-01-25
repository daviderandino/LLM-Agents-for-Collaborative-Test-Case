import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ('a', 1),
    ('ab', 2),
    ('abc', 3),
    ('abcd', 4),
    ('abcabcabc', 3),
    ('abcde', 5),
    ('', 0),
])
def test_find_Rotations_success(str, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_rotation_detection():
    assert find_Rotations('abcabcabc') == 3

def test_find_Rotations_no_rotation_found():
    assert find_Rotations('abcde') == 5

def test_find_Rotations_empty_string():
    assert find_Rotations('') == 0

def test_find_Rotations_none_input():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_non_string_input():
    with pytest.raises(TypeError):
        find_Rotations(123)