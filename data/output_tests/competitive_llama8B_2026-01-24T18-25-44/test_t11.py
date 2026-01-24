import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ("hello", "l", "heo"),
    ("hello", "x", "hello"),
    ("hello", "h", "ello"),
    ("hello", "o", "hell"),
    ("", "a", ""),
    ("a", "a", "")
])
def test_remove_Occ(s, ch, expected):
    assert remove_Occ(s, ch) == expected