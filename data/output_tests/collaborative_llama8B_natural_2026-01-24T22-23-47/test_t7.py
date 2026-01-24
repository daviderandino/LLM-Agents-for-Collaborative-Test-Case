import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),
    ("Code", ["Code"]),
    ("Cat", []),
    ("A Cat Dog", []),
    ("Code Code", ["Code", "Code"]),
    ("", []),
])
def test_find_char_long_success(text, expected):
    assert find_char_long(text) == expected

def test_find_char_long_empty_string():
    assert find_char_long("") == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_non_string_input():
    with pytest.raises(TypeError):
        find_char_long(123)

def test_find_char_long_special_chars_and_numbers():
    assert find_char_long("a1b2c3") == ['a1b2c3']  # Corrected assertion

