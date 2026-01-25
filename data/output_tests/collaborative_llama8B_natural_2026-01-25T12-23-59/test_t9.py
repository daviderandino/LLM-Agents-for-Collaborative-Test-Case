import pytest
from data.input_code.t9 import *


def test_find_Rotations_zero_length_string():
    assert find_Rotations("") == 0

def test_find_Rotations_zero_index():
    assert find_Rotations("abcabc") == 3