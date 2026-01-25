import pytest
from data.input_code.t7 import *


def test_find_char_long_empty_string():
    with pytest.raises(TypeError):
        find_char_long(123)

def test_find_char_long_non_ascii():
    assert find_char_long("café") == ["café"]

def test_find_char_long_punctuation():
    assert find_char_long("Hello.") == ["Hello"]
    assert find_char_long("Hello...") == ["Hello"]

def test_find_char_long_single_word():
    assert find_char_long("Hello") == ["Hello"]

def test_find_char_long_multiple_words():
    assert find_char_long("Hello world") == ["Hello", "world"]