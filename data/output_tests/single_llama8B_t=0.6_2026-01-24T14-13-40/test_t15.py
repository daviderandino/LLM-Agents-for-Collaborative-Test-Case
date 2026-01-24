import pytest

from data.input_code.t15 import split_lowerstring

def test_split_lowerstring_no_match():
    text = "HELLO123"
    assert split_lowerstring(text) == []



def test_split_lowerstring_empty_string():
    text = ""
    assert split_lowerstring(text) == []

def test_split_lowerstring_none_input():
    text = None
    with pytest.raises(TypeError):
        split_lowerstring(text)

def test_split_lowerstring_invalid_input():
    text = 123
    with pytest.raises(TypeError):
        split_lowerstring(text)