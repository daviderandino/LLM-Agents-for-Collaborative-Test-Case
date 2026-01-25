import pytest
from data.input_code.t15 import split_lowerstring

def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []

def test_split_lowerstring_no_lower_case():
    assert split_lowerstring("HELLO123") == []

def test_split_lowerstring_single_lower_case():
    assert split_lowerstring("a") == ["a"]


def test_split_lower_case_with_numbers():
    assert split_lowerstring("a1b2c3") == ["a1", "b2", "c3"]









def test_split_lower_case_with_invalid_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)