import pytest
from data.input_code.t15 import *


def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []


def test_split_lowerstring_uppercase():
    assert split_lowerstring("HELLO WORLD") == []



def test_split_lowerstring_whitespace_only():
    assert split_lowerstring("   ") == []


def test_split_lowerstring_none_input():
    with pytest.raises(TypeError):
        split_lowerstring(None)

def test_split_lowerstring_non_string_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)





def test_split_lowerstring_happy_path_re_whitespace_only():
    assert split_lowerstring("   ") == []

def test_split_lowerstring_happy_path_re_large_input():
    text = "a" * 1000 + "b" * 1000
    assert split_lowerstring(text) == re.findall('[a-z][^a-z]*', text)

def test_split_lowerstring_happy_path_re_mixed_case_large_input():
    text = "a" * 1000 + "b" * 1000
    assert split_lowerstring(text) == re.findall('[a-z][^a-z]*', text)

def test_split_lowerstring_happy_path_re_mixed_case_empty_string():
    assert split_lowerstring("") == []

def test_split_lowerstring_happy_path_re_mixed_case_uppercase():
    assert split_lowerstring("HELLO WORLD") == []

def test_split_lowerstring_happy_path_re_mixed_case_none_input():
    with pytest.raises(TypeError):
        split_lowerstring(None)

def test_split_lowerstring_happy_path_re_mixed_case_non_string_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)