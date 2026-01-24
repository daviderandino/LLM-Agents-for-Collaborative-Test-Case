import pytest
from data.input_code.t14 import *

def test_find_Volume():
    # Test case 1: Positive values
    assert find_Volume(10, 5, 2) == 50.0

    # Test case 2: Zero value
    assert find_Volume(0, 5, 2) == 0.0

    # Test case 3: Negative values
    assert find_Volume(-10, 5, 2) == -50.0

    # Test case 4: Zero length
    assert find_Volume(10, 0, 2) == 0.0

    # Test case 5: Zero breadth
    assert find_Volume(10, 5, 0) == 0.0

    # Test case 6: Zero height
    assert find_Volume(10, 5, 0) == 0.0

    # Test case 7: Large values
    assert find_Volume(100, 50, 20) == 50000.0

    # Test case 8: Large values with negative height
    assert find_Volume(100, 50, -20) == -50000.0

    # Test case 9: Large values with negative length
    assert find_Volume(-100, 50, 20) == -50000.0

    # Test case 10: Large values with negative breadth
    assert find_Volume(100, -50, 20) == -50000.0