import pytest
from data.input_code.t9 import *


def test_find_Rotations_empty_string():
    assert find_Rotations('') == 0

def test_find_Rotations_single_character():
    assert find_Rotations('a') == 1




def test_find_Rotations_string_with_special_chars():
    assert find_Rotations('abc!@#abc') == 9