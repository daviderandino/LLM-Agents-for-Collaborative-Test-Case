import pytest

from data.input_code.t6 import is_Power_Of_Two, differ_At_One_Bit_Pos

def test_is_Power_Of_Two_success():
    # Test case for even number which is a power of 2 (e.g., 8, 16)
    assert is_Power_Of_Two(8)
    # Test case for odd number (not a power of 2)
    assert not is_Power_Of_Two(9)



