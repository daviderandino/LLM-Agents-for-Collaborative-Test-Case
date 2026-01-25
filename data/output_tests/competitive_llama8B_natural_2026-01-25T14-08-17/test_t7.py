import pytest
from data.input_code.t7 import *

def test_find_char_long_happy_path():
    assert find_char_long("Hello world, this is a test") == ['Hello', 'world', 'this', 'test']

def test_find_char_long_empty_text():
    assert find_char_long("") == []



def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_non_string_input():
    with pytest.raises(TypeError):
        find_char_long(123)


