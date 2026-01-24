import pytest
from data.input_code.t15 import *



def test_split_lowerstring_no_matches():
    assert split_lowerstring('HELLO') == []

def test_split_lowerstring_empty_string():
    assert split_lowerstring('') == []

def test_split_lowerstring_none_input():
    with pytest.raises(TypeError):
        split_lowerstring(None)

def test_split_lowerstring_invalid_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)

def test_split_lowerstring_invalid_input_type():
    with pytest.raises(TypeError):
        split_lowerstring([1, 2, 3])