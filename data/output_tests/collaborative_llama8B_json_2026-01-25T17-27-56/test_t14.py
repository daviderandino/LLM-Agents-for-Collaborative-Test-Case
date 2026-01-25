import pytest
from data.input_code.t14 import *

@pytest.mark.parametrize('l, b, h, expected', [
    (5, 3, 2, 15.0),  
    (0, 3, 2, 0.0),
    (10, 3, 2, 30.0),  
    (0, 0, 2, 0.0),
    (0, 3, 0, 0.0),
])
def test_find_Volume_success(l, b, h, expected):
    assert find_Volume(l, b, h) == expected




