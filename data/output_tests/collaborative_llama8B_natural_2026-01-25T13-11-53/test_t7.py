import pytest
from data.input_code.t7 import *
import re

@pytest.mark.parametrize('text, expected', [
    ("Hello World This Is A Test", ["Hello", "World", "This", "Test"]),
    ("Hello Hi There", ["Hello", "There"]),  # Adjusted expected output
    ("Programmers", ["Programmers"]),
    ("", []),
    ("Hello! World", ["Hello", "World"]),
    ("Hello 123 World", ["Hello", "World"]),
    ("...", []),
    ("Test", ["Test"]),
    ("Hello Hello World", ["Hello", "Hello", "World"]),
    ("Café", ["Café"])  # Note: 'Café' is matched because it has 4 characters
])
def test_find_char_long(text, expected):
    assert find_char_long(text) == expected