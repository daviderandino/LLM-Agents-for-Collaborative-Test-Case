import pytest
from data.input_code.t16 import *

def test_text_lowercase_underscore_valid():
    assert text_lowercase_underscore("hello_world") == "Found a match!"

def test_text_lowercase_underscore_invalid():
    assert text_lowercase_underscore("helloWorld") == "Not matched!"

def test_text_lowercase_underscore_non_lowercase():
    assert text_lowercase_underscore("HELLO_WORLD") == "Not matched!"

def test_text_lowercase_underscore_non_underscore_separated():
    assert text_lowercase_underscore("hello world") == "Not matched!"

def test_text_lowercase_underscore_missing_underscore():
    assert text_lowercase_underscore("hello") == "Not matched!"


def test_text_lowercase_underscore_empty_string():
    assert text_lowercase_underscore("") == "Not matched!"

def test_text_lowercase_underscore_none_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)

def test_text_lowercase_underscore_valid_pattern():
    assert text_lowercase_underscore("hello_world") == "Found a match!"

def test_text_lowercase_underscore_invalid_pattern():
    assert text_lowercase_underscore("helloWorld") == "Not matched!"



