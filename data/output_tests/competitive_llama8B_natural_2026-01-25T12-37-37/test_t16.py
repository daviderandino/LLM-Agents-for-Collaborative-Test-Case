import pytest
from data.input_code.t16 import *

def test_text_lowercase_underscore_valid_input():
    assert text_lowercase_underscore('hello_world') == 'Found a match!'

def test_text_lowercase_underscore_invalid_input_case_sensitive():
    assert text_lowercase_underscore('HELLO_WORLD') == 'Not matched!'

def test_text_lowercase_underscore_invalid_input_no_underscore():
    assert text_lowercase_underscore('helloWorld') == 'Not matched!'

def test_text_lowercase_underscore_invalid_input_uppercase_letters():
    assert text_lowercase_underscore('Hello_World') == 'Not matched!'

def test_text_lowercase_underscore_invalid_input_non_alphabetic_characters():
    assert text_lowercase_underscore('hello_World123') == 'Not matched!'

def test_text_lowercase_underscore_empty_string():
    assert text_lowercase_underscore('') == 'Not matched!'

def test_text_lowercase_underscore_none_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)