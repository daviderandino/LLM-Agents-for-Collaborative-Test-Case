import pytest
from data.input_code.t7 import find_char_long


def test_find_char_long_empty_string():
    # Boundary Value: Empty string
    assert find_char_long("") == []

def test_find_char_long_none():
    # Data Type: None
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_min_length_zero():
    # Boundary Value: No 4-letter words in the string
    assert find_char_long("abcd") == ['abcd']


def test_find_char_long_regex_pattern():
    # Regression Test: Test if the regular expression pattern works as expected
    assert find_char_long("ABCD") == ['ABCD']

