import pytest
from data.input_code.t15 import *


def test_split_lowerstring_case_sensitive():
    assert split_lowerstring("HELLO WORLD") == []  # Expected output is empty because the regex pattern only matches lowercase letters


def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []

def test_split_lowerstring_none_input():
    with pytest.raises(TypeError):
        split_lowerstring(None)

def test_split_lowerstring_non_string_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)