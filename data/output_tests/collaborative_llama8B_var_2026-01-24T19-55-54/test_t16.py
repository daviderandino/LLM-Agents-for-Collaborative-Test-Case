import pytest
from data.input_code.t16 import *

def test_text_lowercase_underscore_match():
    assert text_lowercase_underscore('hello_world') == 'Found a match!'

def test_text_lowercase_underscore_not_match_uppercase():
    assert text_lowercase_underscore('Hello World') == 'Not matched!'

def test_text_lowercase_underscore_not_match_non_underscore_separator():
    assert text_lowercase_underscore('hello world') == 'Not matched!'

def test_text_lowercase_underscore_not_match_missing_underscore():
    assert text_lowercase_underscore('hello') == 'Not matched!'

def test_text_lowercase_underscore_not_match_empty_string():
    assert text_lowercase_underscore('') == 'Not matched!'

def test_text_lowercase_underscore_not_match_non_alphabetic_character():
    assert text_lowercase_underscore('hello_world123') == 'Not matched!'

def test_text_lowercase_underscore_not_match_non_underscore_separator():
    assert text_lowercase_underscore('hello world') == 'Not matched!'