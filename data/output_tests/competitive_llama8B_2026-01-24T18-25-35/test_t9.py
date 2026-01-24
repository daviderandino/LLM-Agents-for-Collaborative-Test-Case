import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('input_str, expected', [
    ("abc", 3),  # The rotation length is the length of the string itself
    ("abcd", 4),  # The rotation length is the length of the string itself
    ("", 0),
    ("a", 1)
])
def test_find_Rotations(input_str, expected):
    assert find_Rotations(input_str) == expected

def test_find_Rotations_edge():
    with pytest.raises(TypeError):
        find_Rotations(123)  # Edge case: input is not a string