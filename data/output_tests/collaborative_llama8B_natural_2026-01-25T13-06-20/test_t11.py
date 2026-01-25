import pytest
from data.input_code.t11 import *


def test_remove_Occ_empty_string_and_char():
    assert remove_Occ("", "a") == ""

def test_remove_Occ_single_char_string():
    assert remove_Occ("a", "a") == ""

