import pytest
from data.input_code.t15 import split_lowerstring

def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []


def test_split_lowerstring_no_lower_case():
    assert split_lowerstring("HELLO123") == []




def test_split_lowerstring_invalid_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)

def test_split_lowerstring_non_string_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)


def test_split_lowerstring_no_matches():
    assert split_lowerstring("123456") == []