import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),
    ("This is a test", ["This", "test"]),
    ("Short", ["Short"]),
    ("aaaa", ["aaaa"]),
    ("a", []),
    ("", []),
    (None, [])  # This test should fail because find_char_long() expects a string
])
def test_find_char_long(text, expected):
    if text is None:  # Add a check to ensure text is not None
        pytest.skip("Test is not applicable for None input")
    else:
        result = find_char_long(text)
        assert result == expected

def test_find_char_long_error():
    with pytest.raises(TypeError):
        find_char_long(123)

def test_find_char_long_none():
    with pytest.raises(TypeError):
        find_char_long(None)