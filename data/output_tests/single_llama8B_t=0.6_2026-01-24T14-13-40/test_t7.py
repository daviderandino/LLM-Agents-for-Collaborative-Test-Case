import pytest
from data.input_code.t7 import find_char_long

def test_find_char_long_success():
    text = "Hello world, this is a test with 4 and 5 letter words."
    result = find_char_long(text)
    assert len(result) > 0

def test_find_char_long_empty_string():
    text = ""
    result = find_char_long(text)
    assert result == []

def test_find_char_long_no_matches():
    text = "a b c"
    result = find_char_long(text)
    assert result == []


def test_find_char_long_empty_list():
    text = ""
    result = find_char_long(text)
    assert result == []

def test_find_char_long_none_input():
    text = None
    with pytest.raises(TypeError):
        find_char_long(text)

def test_find_char_long_max_match():
    text = "abcde abcde abcde"
    result = find_char_long(text)
    assert len(result) == 3

def test_find_char_long_min_match():
    text = "abcd abcd abcd"
    result = find_char_long(text)
    assert len(result) == 3