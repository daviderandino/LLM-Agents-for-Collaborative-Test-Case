import pytest
from data.input_code.t16 import text_lowercase_underscore

def test_text_lowercase_underscore_success():
    assert text_lowercase_underscore('hello_world') == 'Found a match!'

def test_text_lowercase_underscore_failure():
    assert text_lowercase_underscore('HelloWorld') == 'Not matched!'

def test_text_lowercase_underscore_empty_string():
    assert text_lowercase_underscore('') == 'Not matched!'


def test_text_lowercase_underscore_no_underscore():
    assert text_lowercase_underscore('helloworld') == 'Not matched!'

def test_text_lowercase_underscore_first_char_uppercase():
    assert text_lowercase_underscore('Hellow_world') == 'Not matched!'

def test_text_lowercase_underscore_last_char_uppercase():
    assert text_lowercase_underscore('hello_World') == 'Not matched!'


def test_text_lowercase_underscore_invalid_pattern():
    assert text_lowercase_underscore('Hello World') == 'Not matched!'