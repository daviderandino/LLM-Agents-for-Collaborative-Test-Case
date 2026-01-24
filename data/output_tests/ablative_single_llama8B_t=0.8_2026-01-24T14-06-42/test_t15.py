import pytest
from data.input_code.t15 import split_lowerstring


def test_split_lowerstring_empty_string():
    text = ""
    result = split_lowerstring(text)
    assert result == []


def test_split_lowerstring_single_upper_string_fails():
    text = "HELLO"
    result = split_lowerstring(text)
    assert result == []

def test_split_lowerstring_string_with_no_letters():
    text = "123456"
    result = split_lowerstring(text)
    assert result == []


def test_split_lowerstring_string_with_no_letters_or_spaces():
    text = "1234567890"
    result = split_lowerstring(text)
    assert result == []



