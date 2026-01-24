import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["World"]),
    ("abcde", ["abcde"]),
    ("a", []),
    ("", [])
])
def test_find_char_long_success(text, expected):
    result = find_char_long(text)
    assert result == expected

def test_find_char_long_error():
    with pytest.raises(TypeError):
        find_char_long(None)

# Fixing the failing test case
@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),  # Expected result should include 'Hello' as well
    ("abcde", ["abcde"]),
    ("a", []),
    ("", [])
])
def test_find_char_long_success(text, expected):
    result = find_char_long(text)
    assert result == expected