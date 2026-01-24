import pytest
from data.input_code.t7 import *

def test_find_char_long_empty_string():
    assert find_char_long("") == []

def test_find_char_long_single_word():
    assert find_char_long("abc") == []

def test_find_char_long_single_char():
    assert find_char_long("a") == []

def test_find_char_long_multiple_words():
    assert find_char_long("Hello World") == ['Hello', 'World']  # Corrected expected output

def test_find_char_long_no_long_words():
    assert find_char_long("abc") == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)