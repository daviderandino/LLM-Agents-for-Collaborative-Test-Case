import pytest
from data.input_code.t7 import *


def test_find_char_long_empty_text():
    assert find_char_long("") == []

def test_find_char_long_whitespace_text():
    assert find_char_long("   ") == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_non_string_input():
    with pytest.raises(TypeError):
        find_char_long(123)