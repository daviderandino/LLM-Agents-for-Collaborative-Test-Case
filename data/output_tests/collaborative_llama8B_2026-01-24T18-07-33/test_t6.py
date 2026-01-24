import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False),
    (0, False),
    (-8, False)
])
def test_is_Power_Of_Two(x, expected):
    assert is_Power_Of_Two(x) == expected

