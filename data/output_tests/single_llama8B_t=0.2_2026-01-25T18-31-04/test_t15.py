import pytest
from data.input_code.t15 import split_lowerstring

def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []

def test_split_lowerstring_no_lower_case():
    assert split_lowerstring("HELLO123") == []

def test_split_lowerstring_no_characters():
    assert split_lowerstring("123456") == []

def test_split_lowerstring_single_lower_case():
    assert split_lowerstring("a") == ["a"]





