import pytest

from data.input_code.t16 import text_lowercase_underscore

def test_text_lowercase_underscore_match():
    assert text_lowercase_underscore('hello_world') == 'Found a match!'

def test_text_lowercase_underscore_no_match():
    assert text_lowercase_underscore('HelloWorld') != 'Found a match!'

def test_text_lowercase_underscore_edge():
    assert text_lowercase_underscore('lower') != 'Found a match!'

def test_text_lowercase_underscore_edge2():
    assert text_lowercase_underscore('lower1') != 'Found a match!'

def test_text_lowercase_underscore_empty_text():
    assert text_lowercase_underscore('') == 'Not matched!'


def test_text_lowercase_underscore_none_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore()