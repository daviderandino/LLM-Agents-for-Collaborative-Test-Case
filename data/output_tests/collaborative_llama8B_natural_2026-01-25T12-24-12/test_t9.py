import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("abcabc", 3),  # Corrected the expected value
    ("ab", 2),
    ("", 0),
    ("a", 1),
    ("a", 1),
    ("abcde", 5),
    ("a"*10000, 1)
])
def test_find_Rotations(str, expected):
    assert find_Rotations(str) == expected

