import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('input_str, expected', [
    ("abcabc", 3),
    ("abc", 3),
    ("", 0),
    ("a", 1)
])
def test_find_Rotations(input_str, expected):
    assert find_Rotations(input_str) == expected