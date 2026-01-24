import pytest
from data.input_code.t11 import *

def test_remove_Occ_success():
    assert remove_Occ("Hello World", "o") == "Hell Wrld"
    assert remove_Occ("", "a") == ""
    assert remove_Occ("Hello World", "z") == "Hello World"

def test_remove_Occ_error_non_existent():
    assert remove_Occ("Hello World", "z") == "Hello World"

def test_remove_Occ_error_empty_string():
    assert remove_Occ("", "a") == ""

def test_remove_Occ_error_none_input():
    with pytest.raises(TypeError):
        remove_Occ(None, "a")


def test_remove_Occ_error_non_string_input_2():
    with pytest.raises(TypeError):
        remove_Occ(123, "a")




