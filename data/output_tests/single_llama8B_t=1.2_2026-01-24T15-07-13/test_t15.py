import pytest
from data.input_code.t15 import split_lowerstring

def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []


def test_split_lowerstring_no_lowercase():
    assert split_lowerstring("ABC123") == []

def test_split_lowerstring_no_special_chars():
    assert split_lowerstring("hello") == ['h', 'e', 'l', 'l', 'o']

def test_split_lowerstring_single_lowercase_with_special_chars():
    assert split_lowerstring("a!") == ['a!']




