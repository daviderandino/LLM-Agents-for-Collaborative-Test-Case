import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ("Hello World", "o", "Hell Wrld"),
    ("Hello World", "O", "Hello World"),
    ("", "a", ""),
    ("Hello World", "!", "Hello World")
])
def test_remove_Occ(s, ch, expected):
    assert remove_Occ(s, ch) == expected