import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ("hello_world", "Found a match!"),
    ("HelloWorld", "Not matched!"),
    ("", "Not matched!"),
    ("Hello World", "Not matched!"),
    ("123", "Not matched!"),
    ("hello", "Not matched!")
])
def test_text_lowercase_underscore(text, expected):
    assert text_lowercase_underscore(text) == expected