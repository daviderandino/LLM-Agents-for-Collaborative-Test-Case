import pytest
from data.input_code.t7 import *


def test_find_char_long_error():
    with pytest.raises(TypeError):
        find_char_long(None)

# Fix the assertion for the test case "Hello World"
@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),  # Corrected expected result
    ("abcde", ["abcde"]),
    ("a", []),
    ("", [])
])
def test_find_char_long_success_corrected(text, expected):
    result = find_char_long(text)
    assert result == expected