import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("abcabc", 3),
    ("abcdef", 6),
    ("", 0),
    ("a", 1)
])
def test_find_Rotations(str, expected):
    assert find_Rotations(str) == expected