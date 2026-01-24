import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),
    ("This is a test", ["This", "test"]),
    ("Short", ["Short"]),
    ("aaaa", ["aaaa"]),
    ("aaaaa", ["aaaaa"]),
    ("", []),
    ("123", [])  # This will raise a TypeError
])
def test_find_char_long(text, expected):
    result = find_char_long(text)
    assert result == expected

def test_find_char_long_error():
    with pytest.raises(TypeError):
        find_char_long(123)

def test_find_char_long_none():
    with pytest.raises(TypeError):
        find_char_long(None)

