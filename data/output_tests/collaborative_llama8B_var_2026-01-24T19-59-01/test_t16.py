import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ("hello_world", "Found a match!"),
    ("Hello World", "Not matched!"),
    ("hello_world123", "Not matched!"),
    ("", "Not matched!"),
    ("HELLO_WORLD", "Not matched!"),
    ("hello", "Not matched!"),
    ("hello_world1234", "Not matched!"),
    ("hello world", "Not matched!")
])
def test_text_lowercase_underscore(text, expected):
    assert text_lowercase_underscore(text) == expected