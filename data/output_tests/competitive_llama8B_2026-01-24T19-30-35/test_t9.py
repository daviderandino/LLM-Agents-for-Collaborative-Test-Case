import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('input_str, expected', [
    ("abc", 3),  # The rotation length is the length of the string
    ("abcd", 4),  # The rotation length is the length of the string
    ("", 0),
    ("a", 1)
])
def test_find_Rotations_success(input_str, expected):
    assert find_Rotations(input_str) == expected

def test_find_Rotations_error():
    with pytest.raises(TypeError):
        find_Rotations(123)  # Test with non-string input

def test_find_Rotations_empty_string():
    assert find_Rotations("") == 0