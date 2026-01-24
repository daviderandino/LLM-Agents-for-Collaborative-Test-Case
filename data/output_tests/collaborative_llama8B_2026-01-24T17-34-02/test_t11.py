import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ("Hello World", "o", "Hell Wrld"),
    ("Hello World", "z", "Hello World"),
    ("", "a", ""),
])
def test_remove_Occ_success(s, ch, expected):
    assert remove_Occ(s, ch) == expected





def test_remove_Occ_error_empty_string_input():
    assert remove_Occ("", "a") == ""

def test_remove_Occ_error_single_char_input():
    assert remove_Occ("a", "a") == ""

def test_remove_Occ_error_multiple_chars_input():
    assert remove_Occ("aa", "a") == ""

def test_remove_Occ_error():
    assert remove_Occ("Hello World", "o") == "Hell Wrld"