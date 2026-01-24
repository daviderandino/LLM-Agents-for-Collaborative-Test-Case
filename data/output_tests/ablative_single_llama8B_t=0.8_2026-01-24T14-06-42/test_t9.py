import pytest

from data.input_code.t9 import find_Rotations

def test_find_Rotations_positive():
    assert find_Rotations("abcabcabc") == 3


def test_find_Rotations_single_character():
    assert find_Rotations("a") == 1

def test_find_Rotations_single_character_rotation():
    assert find_Rotations("aa") == 1


def test_find_Rotations_rotated_once():
    assert find_Rotations("bdcab") == 5

def test_find_Rotations_rotated_multiple_times():
    assert find_Rotations("abcabcabc") == 3

