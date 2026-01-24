import pytest
from data.input_code.t11 import remove_Occ

def test_remove_Occ_success():
    # Test removing a character from a string
    assert remove_Occ("hello", "l") == "heo"
    assert remove_Occ("world", "d") == "worl"
    assert remove_Occ("python", "o") == "pythn"

def test_remove_Occ_empty_string():
    # Test removing a character from an empty string
    assert remove_Occ("", "a") == ""

def test_remove_Occ_not_found():
    # Test removing a character not present in the string
    assert remove_Occ("hello", "x") == "hello"

def test_remove_Occ_multiple_occurrences():
    # Test removing multiple occurrences of a character
    assert remove_Occ("hello", "l") == "heo"
    assert remove_Occ("hello", "l") == "heo"  # Second call should not change the result

def test_remove_Occ_edge_case():
    # Test removing the only occurrence of a character
    assert remove_Occ("a", "a") == ""

def test_remove_Occ_edge_case_multiple_chars():
    # Test removing all occurrences of multiple characters
    assert remove_Occ("hello", "l") == "heo"
    assert remove_Occ("hello", "h") == "ello"
    assert remove_Occ("hello", "o") == "hell"
    assert remove_Occ("hello", "l") == "heo"  # Second call should not change the result

