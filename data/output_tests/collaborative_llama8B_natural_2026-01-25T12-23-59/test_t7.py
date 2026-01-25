import pytest
from text import *

def find_words_longer_than_3_chars(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    words = input_string.split()
    return [word for word in words if len(word) > 3]

@pytest.mark.parametrize('text, expected', [
    ("Hello world this is a test", ["world", "test"]),
    ("Programmer", ["Programmer"]),
    ("Hello", []),
    ("Programmers developers engineers", ["Programmers", "developers", "engineers"]),
    ("", []),
])
def test_find_words_longer_than_3_chars_success(text, expected):
    assert find_words_longer_than_3_chars(text) == expected

def test_find_words_longer_than_3_chars_empty_string():
    assert find_words_longer_than_3_chars("") == []

def test_find_words_longer_than_3_chars_none_input():
    with pytest.raises(TypeError):
        find_words_longer_than_3_chars(None)

def test_find_words_longer_than_3_chars_non_string_input():
    with pytest.raises(TypeError):
        find_words_longer_than_3_chars(123)

def test_find_words_longer_than_3_chars_special_characters():
    assert find_words_longer_than_3_chars("abc!@#") == []

def test_find_words_longer_than_3_chars_punctuation_handling():
    assert find_words_longer_than_3_chars("Hello, world") == ["Hello", "world"]