import pytest
from data.input_code.t6 import is_Power_Of_Two, differ_At_One_Bit_Pos

def test_is_Power_Of_Two():
    # Test Power of Two
    assert is_Power_Of_Two(8) == True
    # Test Not Power of Two
    assert is_Power_Of_Two(10) == False
    # Test Zero
    assert is_Power_Of_Two(0) == False
    # Test Negative Number
    assert is_Power_Of_Two(-8) == False
    # Test Edge Case: One
    assert is_Power_Of_Two(1) == True

