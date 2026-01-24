import pytest

from data.input_code.t11 import remove_Occ

def test_remove_Occ_success():
    # Test removing a character from a string
    s = "Hello, World!"
    ch = "o"
    expected_result = "Hell, Wrld!"
    assert remove_Occ(s, ch) == expected_result

def test_remove_Occ_empty_string():
    # Test removing from an empty string
    s = ""
    ch = "a"
    assert remove_Occ(s, ch) == ""


def test_remove_Occ_single_char():
    # Test removing a single character
    s = "Hello, World!"
    ch = "!"
    expected_result = "Hello, World"
    assert remove_Occ(s, ch) == expected_result

def test_remove_Occ_last_char():
    # Test removing the last character
    s = "Hello, World!"
    ch = "!"
    expected_result = "Hello, World"
    assert remove_Occ(s, ch) == expected_result


def test_remove_Occ_ch_is_none():
    # Test passing None as the character to remove
    s = "Hello, World!"
    ch = None
    assert remove_Occ(s, ch) == s

def test_remove_Occ_ch_is_empty_string():
    # Test passing an empty string as the character to remove
    s = "Hello, World!"
    ch = ""
    assert remove_Occ(s, ch) == s


def test_remove_Occ_s_is_empty_string_ch_is_none():
    # Test passing an empty string and None as the character
    s = ""
    ch = None
    assert remove_Occ(s, ch) == ""