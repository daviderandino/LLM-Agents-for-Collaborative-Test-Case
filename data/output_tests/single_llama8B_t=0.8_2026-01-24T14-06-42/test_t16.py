import pytest
from data.input_code.t16 import text_lowercase_underscore

def test_text_lowercase_underscore_success():
    """Test a successful match"""
    assert text_lowercase_underscore("hello_world") == 'Found a match!'

def test_text_lowercase_underscore_failure():
    """Test a failed match"""
    assert text_lowercase_underscore("HelloWorld") == 'Not matched!'

def test_text_lowercase_underscore_empty_string():
    """Test an empty string"""
    assert text_lowercase_underscore("") == 'Not matched!'




def test_text_lowercase_underscore_pattern_invalid_chars():
    """Test a string with invalid characters"""
    assert text_lowercase_underscore("HelloWorld123") == 'Not matched!'

def test_text_lowercase_underscore_pattern_whitespace():
    """Test a string with whitespace"""
    assert text_lowercase_underscore("hello world") == 'Not matched!'