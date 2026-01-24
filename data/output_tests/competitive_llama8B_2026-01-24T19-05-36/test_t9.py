import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('input_str, expected', [
    ("abc", 3),
    ("abcd", 4),
    ("", 0),
    ("a", 1)
])
def test_find_Rotations_success(input_str, expected):
    assert find_Rotations(input_str) == expected

def test_find_Rotations_error():
    with pytest.raises(TypeError):
        find_Rotations(None)