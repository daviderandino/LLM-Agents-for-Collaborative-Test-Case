import pytest
from data.input_code.t9 import find_Rotations

# Edge cases for min, max rotations
def test_min_rotation():
    assert find_Rotations('a') == 1

def test_max_rotation():
    assert find_Rotations('abc') == len('abc')

def test_max_single_char_rotation():
    assert find_Rotations('a') == 1

# Rotation at a position where the string appears twice in the doubled string

# Rotations not found in the doubled string

# Rotation at the exact position where the string is present in the doubled string at position 1 
# Test empty string with 0 length 
