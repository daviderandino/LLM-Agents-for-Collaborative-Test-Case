import pytest
from data.input_code.t16 import *

def test_text_lowercase_underscore_match():
    assert text_lowercase_underscore("hello_world") == "Found a match!"

def test_text_lowercase_underscore_no_match():
    assert text_lowercase_underscore("HelloWorld") == "Not matched!"

def test_text_lowercase_underscore_empty():
    assert text_lowercase_underscore("") == "Not matched!"

def test_text_lowercase_underscore_invalid():
    assert text_lowercase_underscore("Hello World") == "Not matched!"

def test_text_lowercase_underscore_invalid_pattern():
    assert text_lowercase_underscore("123abc") == "Not matched!"

def test_text_lowercase_underscore_start_with_digit():
    assert text_lowercase_underscore("1hello_world") == "Not matched!"

def test_text_lowercase_underscore_multiple_underscores():
    assert text_lowercase_underscore("hello_world_hello_world") == "Not matched!"

def test_text_lowercase_underscore_uppercase():
    assert text_lowercase_underscore("HelloWorld") == "Not matched!"

def test_text_lowercase_underscore_special_characters():
    assert text_lowercase_underscore("hello_world!@#") == "Not matched!"

def test_text_lowercase_underscore_numbers_and_letters():
    assert text_lowercase_underscore("hello123_world") == "Not matched!"