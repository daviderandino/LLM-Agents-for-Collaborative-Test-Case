import pytest
from data.input_code.t15 import *


def test_split_lowerstring_error():
    with pytest.raises(TypeError):
        split_lowerstring(None)

def test_split_lowerstring_empty_string():
    result = split_lowerstring("")
    assert result == []

def test_split_lowerstring_single_lowercase_letter():
    result = split_lowerstring("a")
    assert result == ["a"]


def test_split_lowerstring_multiple_lowercase_letters():
    result = split_lowerstring("abc")
    assert result == ["a", "b", "c"]


# Fix the assertions in the test code so they match the Source Code logic and PASS



