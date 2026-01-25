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

def test_remove_Occ_remove_first_occurrence():
    # Test removing the first occurrence of a character
    assert remove_Occ("hello", "h") == "ello"

def test_remove_Occ_remove_last_occurrence():
    # Test removing the last occurrence of a character
    assert remove_Occ("hello", "o") == "hell"

def test_remove_Occ_remove_all_occurrences():
    # Test removing all occurrences of a character
    assert remove_Occ("hello", "l") == "heo"

def test_remove_Occ_remove_all_characters():
    # Test removing all characters from the string
    assert remove_Occ("hello", "h") == "ello"

def test_remove_Occ_input_type_error():
    # Test passing a non-string input
    with pytest.raises(TypeError):
        remove_Occ(123, "a")



