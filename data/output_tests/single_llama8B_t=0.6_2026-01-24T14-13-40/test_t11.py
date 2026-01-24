import pytest

from data.input_code.t11 import remove_Occ

def test_remove_Occ_success():
    # Test removing a character from a string
    assert remove_Occ("hello", "l") == "heo"
    assert remove_Occ("hello", "h") == "ello"

def test_remove_Occ_empty_string():
    # Test removing a character from an empty string
    assert remove_Occ("", "a") == ""

def test_remove_Occ_no_occurrences():
    # Test removing a character that does not occur in the string
    assert remove_Occ("hello", "x") == "hello"

def test_remove_Occ_multiple_occurrences():
    # Test removing multiple occurrences of a character
    assert remove_Occ("hello", "l") == "heo"
    assert remove_Occ("hello", "l") == "heo"  # Second call should not change the result

def test_remove_Occ_empty_string_and_char():
    # Test removing a character from an empty string and character
    assert remove_Occ("", "") == ""

def test_remove_Occ_char_only():
    # Test removing a character from a string containing only one character
    assert remove_Occ("a", "a") == ""
    assert remove_Occ("a", "b") == "a"

