import pytest
from data.input_code.t7 import *


def test_find_char_long_empty_text():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_non_string_input():
    with pytest.raises(TypeError):
        find_char_long(123)

def test_find_char_long_special_characters_handling():
    assert find_char_long("hello! world, python#") == ["hello", "world", "python"]

def test_find_char_long_non_ascii_characters_handling():
    assert find_char_long("héllo world") == ["héllo", "world"]

def test_find_char_long_punctuation_handling():
    assert find_char_long("hello, world") == ["hello", "world"]


def test_find_char_long_empty_string():
    assert find_char_long("") == []

def test_find_char_long_multiple_spaces():
    assert find_char_long("   hello   world   ") == ["hello", "world"]