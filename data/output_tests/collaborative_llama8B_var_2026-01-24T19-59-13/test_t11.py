import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ("Hello World", "o", "Hell Wrld"),
    ("Hello World", "z", "Hello World"),
    ("", "o", ""),
])
def test_remove_Occ_success(s, ch, expected):
    assert remove_Occ(s, ch) == expected

















