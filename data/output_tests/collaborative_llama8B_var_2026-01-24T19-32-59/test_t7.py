import pytest
from data.input_code.t7 import *


def test_find_char_long_error():
    with pytest.raises(TypeError):
        find_char_long(123)

def test_find_char_long_none():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_empty_string():
    assert find_char_long("") == []

def test_find_char_long_single_char():
    assert find_char_long("a") == []

def test_find_char_long_four_chars():
    assert find_char_long("aaaa") == ["aaaa"]

def test_find_char_long_longer_than_four_chars():
    assert find_char_long("Hello") == ["Hello"]

def test_find_char_long_multiple_words():
    assert find_char_long("Hello World") == ["Hello", "World"]