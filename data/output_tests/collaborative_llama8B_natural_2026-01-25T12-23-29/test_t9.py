import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("hello", 5),
    ("abcabc", 3),
    ("", 0),
    ("a", 1),
    ("abcabc", 3),
    ("a"*1000, 1),
    ("abba", 4)
])
def test_find_Rotations(str, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_not_rotation():
    with pytest.raises(AssertionError):
        assert find_Rotations("hello") == 6