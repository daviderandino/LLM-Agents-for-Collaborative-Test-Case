import pytest
from data.input_code.t11 import *

def test_remove_Occ_happy_path():
    assert remove_Occ("hello", "l") == "heo"

def test_remove_Occ_no_change():
    assert remove_Occ("hello", "x") == "hello"

def test_remove_Occ_single_character():
    assert remove_Occ("a", "a") == ""

def test_remove_Occ_empty_string():
    assert remove_Occ("", "a") == ""

def test_remove_Occ_duplicate_characters():
    assert remove_Occ("helloo", "o") == "hell"

def test_remove_Occ_character_at_start():
    assert remove_Occ("hello", "h") == "ello"

def test_remove_Occ_character_at_end():
    assert remove_Occ("hello", "o") == "hell"

def test_remove_Occ_character_in_middle():
    assert remove_Occ("hello", "l") == "heo"

def test_remove_Occ_single_occurrence():
    assert remove_Occ("hello", "l") == "heo"

def test_remove_Occ_multiple_occurrences_at_start():
    assert remove_Occ("lllllo", "l") == "lllo"

def test_remove_Occ_multiple_occurrences_at_end():
    assert remove_Occ("helloo", "o") == "hell"


def test_remove_Occ_invalid_input_type():
    with pytest.raises(TypeError):
        remove_Occ(123, "a")

