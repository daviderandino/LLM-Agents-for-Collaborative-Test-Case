import pytest

from data.input_code.t14 import find_Volume

@pytest.mark.parametrize(
    "length, breadth, height, expected_output", [
        (1, 2, 3, 3),
        (10, 2, 3, 30),
        (10, 0, 2, 0) 
    ]
)
def test_find_volume(length, breadth, height, expected_output):
    assert find_Volume(length, breadth, height) == expected_output



def test_find_volume_zero_inputs():
    assert find_Volume(0, 0, 0) == 0


def test_find_volume_negative_number():
    assert find_Volume(-1, 0, 0) == 0

import math

