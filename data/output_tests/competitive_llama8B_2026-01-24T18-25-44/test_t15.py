import pytest
from data.input_code.t15 import *


def test_split_lowerstring_error():
    with pytest.raises(TypeError):
        split_lowerstring(123)

def test_split_lowerstring_empty_string():
    assert split_lowerstring("   ") == []

def test_split_lowerstring_single_char():
    assert split_lowerstring("a") == ["a"]

def test_split_lowerstring_single_char_with_non_alphabetic():
    assert split_lowerstring("a1") == ["a1"]


