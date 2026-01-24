import pytest
from data.input_code.t11 import remove_Occ

def test_remove_Occ_success():
    # Test removing a character from a string
    assert remove_Occ("hello", "l") == "heo"

def test_remove_Occ_empty_string():
    # Test removing a character from an empty string
    assert remove_Occ("", "a") == ""

def test_remove_Occ_no_occurrence():
    # Test removing a character that does not occur in the string
    assert remove_Occ("hello", "x") == "hello"

def test_remove_Occ_remove_from_start():
    # Test removing a character from the start of the string
    assert remove_Occ("hello", "h") == "ello"

def test_remove_Occ_remove_from_end():
    # Test removing a character from the end of the string
    assert remove_Occ("hello", "o") == "hell"

def test_remove_Occ_remove_from_middle():
    # Test removing a character from the middle of the string
    assert remove_Occ("hello", "l") == "heo"

def test_remove_Occ_remove_all_occurrences():
    # Test removing all occurrences of a character
    assert remove_Occ("hello", "l") == "heo"


