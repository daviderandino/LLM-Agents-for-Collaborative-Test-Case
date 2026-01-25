import pytest
from data.input_code.t16 import *

def test_text_lowercase_underscore_happy_path():
    assert text_lowercase_underscore('hello_world') == 'Found a match!'

def test_text_lowercase_underscore_case_sensitivity():
    assert text_lowercase_underscore('Hello_World') == 'Not matched!'

def test_text_lowercase_underscore_pattern_non_matching():
    assert text_lowercase_underscore('Hello World') == 'Not matched!'

def test_text_lowercase_underscore_empty_input():
    assert text_lowercase_underscore('') == 'Not matched!'

def test_text_lowercase_underscore_none_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)

def test_text_lowercase_underscore_leading_digit():
    assert text_lowercase_underscore('1hello_world') == 'Not matched!'

def test_text_lowercase_underscore_uppercase_letters_with_underscore():
    assert text_lowercase_underscore('Hello_world') == 'Not matched!'

def test_text_lowercase_underscore_single_underscore():
    assert text_lowercase_underscore('hello_world_') == 'Not matched!'

def test_text_lowercase_underscore_multiple_consecutive_underscores():
    assert text_lowercase_underscore('hello_world__') == 'Not matched!'

def test_text_lowercase_underscore_special_characters():
    assert text_lowercase_underscore('hello@world') == 'Not matched!'