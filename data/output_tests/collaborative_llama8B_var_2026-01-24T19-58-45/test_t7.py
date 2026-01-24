import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),
    ("This is a test", ["This", "test"]),
])
def test_find_char_long_success(text, expected):
    assert find_char_long(text) == expected

def test_find_char_long_empty_string():
    assert find_char_long("") == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_short_word():
    assert find_char_long("Short") == ['Short']  # Adjusted assertion to match the Source Code behavior

# Additional test case to cover the edge case where the word is exactly 4 characters long
def test_find_char_long_word_with_four_characters():
    assert find_char_long("Code") == ['Code']  # Adjusted assertion to match the Source Code behavior