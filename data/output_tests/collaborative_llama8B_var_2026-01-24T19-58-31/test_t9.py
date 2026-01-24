import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ("abc", 3),
    ("abcd", 4),
])
def test_find_Rotations_success(str, expected):
    assert find_Rotations(str) == expected

def test_find_Rotations_edge_case_self_rotation():
    assert find_Rotations("abcabc") == 3

def test_find_Rotations_edge_case_empty_string():
    assert find_Rotations("") == 0

def test_find_Rotations_edge_case_single_character():
    assert find_Rotations("a") == 1