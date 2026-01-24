import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ("Hello World", "o", "Hell Wrld"),
    ("Hello World", "z", "Hello World"),
    ("Hello World", "H", "ello World"),
    ("Hello World", "W", "Hello orld"),
    ("", "a", ""),
    ("a", "a", "")
])
def test_remove_Occ(s, ch, expected):
    assert remove_Occ(s, ch) == expected


def test_remove_Occ_empty_string():
    assert remove_Occ("", "a") == ""

def test_remove_Occ_single_char_string():
    assert remove_Occ("a", "a") == ""


def test_remove_Occ_multiple_occurrences_from_end():
    assert remove_Occ("Hello World", "o") == "Hell Wrld"

def test_remove_Occ_multiple_occurrences_from_start():
    assert remove_Occ("Hello World", "H") == "ello World"

def test_remove_Occ_multiple_occurrences_from_both_ends():
    assert remove_Occ("Hello World", "o") == "Hell Wrld"

