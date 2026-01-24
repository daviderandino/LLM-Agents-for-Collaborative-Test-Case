import pytest
from data.input_code.t11 import remove_Occ


def test_remove_Occ_empty_string():
    # Test removing a character from an empty string
    assert remove_Occ("", "a") == ""

def test_remove_Occ_no_occurrences():
    # Test removing a character with no occurrences
    assert remove_Occ("Hello World", "x") == "Hello World"


def test_remove_Occ_remove_first_occurrence():
    # Test removing the first occurrence of a character
    assert remove_Occ("Hello World", "H") == "ello World"

def test_remove_Occ_remove_last_occurrence():
    # Test removing the last occurrence of a character
    assert remove_Occ("Hello World", "d") == "Hello Worl"

def test_remove_Occ_remove_middle_occurrence():
    # Test removing a character that appears in the middle of the string
    assert remove_Occ("Hello World", "o") == "Hell Wrld"


