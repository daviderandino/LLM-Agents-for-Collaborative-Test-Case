import pytest
from data.input_code.t11 import remove_Occ


def test_remove_Occ_empty_string():
    assert remove_Occ("", "o") == ""

def test_remove_Occ_no_O():
    assert remove_Occ("Hello World", "x") == "Hello World"





