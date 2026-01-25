import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ('abc', 3),
    ('aaa', 1),
    ('abcd', 4),
    ('', 0),
    ('a', 1),
    ('a' * 100, 1),
])
def test_find_Rotations_success(str, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_error_none():
    with pytest.raises(TypeError):
        find_Rotations(None)

def test_find_Rotations_error_non_string():
    with pytest.raises(TypeError):
        find_Rotations(123)

def test_find_Rotations_error_special_chars():
    assert find_Rotations('abc!') == 4