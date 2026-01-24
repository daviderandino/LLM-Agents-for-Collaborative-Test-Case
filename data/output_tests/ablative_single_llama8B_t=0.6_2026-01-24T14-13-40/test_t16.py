import pytest
from data.input_code.t16 import text_lowercase_underscore

def test_text_lowercase_underscore_match():
    text = 'hello_world'
    result = text_lowercase_underscore(text)
    assert result == 'Found a match!'

def test_text_lowercase_underscore_no_match():
    text = 'HelloWorld'
    result = text_lowercase_underscore(text)
    assert result == 'Not matched!'

def test_text_lowercase_underscore_empty_string():
    text = ''
    result = text_lowercase_underscore(text)
    assert result == 'Not matched!'

def test_text_lowercase_underscore_none():
    text = None
    with pytest.raises(TypeError):
        text_lowercase_underscore(text)

def test_text_lowercase_underscore_invalid_pattern():
    text = 'helloWorld'
    result = text_lowercase_underscore(text)
    assert result == 'Not matched!'

