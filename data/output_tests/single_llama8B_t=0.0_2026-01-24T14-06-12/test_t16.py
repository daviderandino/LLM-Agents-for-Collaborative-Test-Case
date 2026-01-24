import pytest
from data.input_code.t16 import text_lowercase_underscore

def test_text_lowercase_underscore_match():
    assert text_lowercase_underscore('hello_world') == 'Found a match!'

def test_text_lowercase_underscore_no_match():
    assert text_lowercase_underscore('HelloWorld') == 'Not matched!'

def test_text_lowercase_underscore_empty_string():
    assert text_lowercase_underscore('') == 'Not matched!'





def test_text_lowercase_underscore_invalid_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore(123)

def test_text_lowercase_underscore_invalid_pattern_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore('hello_world', 123)