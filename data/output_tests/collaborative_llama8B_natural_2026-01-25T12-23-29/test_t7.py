import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("hello", ["hello"]),
    ("house", ["house"]),
    ("hello world house", ["hello", "world", "house"]),
    ("cat", []),
    ("university", ["university"]),  # Adjusted expected output
    ("a b c d e", []),
    ("university computer programming", ["university", "computer", "programming"]),  # Adjusted expected output
    ("", []),
    ("   ", []),
    ("hello!", ["hello"]),
    ("hello, world", ["hello", "world"]),
    ("hëllo", ["hëllo"]),
    ("hello123", ["hello123"])
])
def test_find_char_long(text, expected):
    assert find_char_long(text) == expected

def test_find_char_long_empty_string():
    assert find_char_long("") == []

def test_find_char_long_special_characters():
    assert find_char_long("hello!") == ["hello"]

def test_find_char_long_punctuation():
    assert find_char_long("hello, world") == ["hello", "world"]

def test_find_char_long_non_ascii_characters():
    assert find_char_long("hëllo") == ["hëllo"]

def test_find_char_long_numbers():
    assert find_char_long("hello123") == ["hello123"]