import pytest
from data.input_code.t14 import find_Volume

def test_find_Volume_success_cases():
    # Test with positive numbers
    assert find_Volume(2, 3, 4) == (2 * 3 * 4) / 2
    assert find_Volume(10, 5, 1) == (10 * 5 * 1) / 2
    # Test with zero and non-zero numbers
    assert find_Volume(0, 3, 4) == 0
    assert find_Volume(2, 0, 4) == 0
    assert find_Volume(2, 3, 0) == 0
    # Test with very large numbers
    assert find_Volume(1000000, 500000, 100) == (1000000 * 500000 * 100) / 2

def test_find_Volume_invalid_input_type():
    # Test with non-numeric input
    with pytest.raises(TypeError):
        find_Volume(2, 'a', 4)
    with pytest.raises(TypeError):
        find_Volume('b', 3, 4)
    with pytest.raises(TypeError):
        find_Volume(2, 3, 'c')



def test_find_Volume_invalid_number_of_args():
    # Test with input arguments other than 3
    with pytest.raises(TypeError):
        find_Volume(2)
    with pytest.raises(TypeError):
        find_Volume(2, 3)
    with pytest.raises(TypeError):
        find_Volume(2, 3, 4, 5, 6)